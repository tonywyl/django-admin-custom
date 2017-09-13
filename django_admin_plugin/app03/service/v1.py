from django.shortcuts import HttpResponse,render,redirect
from django.urls import reverse
from types import FunctionType
from django.utils.safestring import mark_safe
from django.forms.boundfield import BoundField
from django.forms.models import ModelFormMetaclass
from django.forms.models import ModelMultipleChoiceField
from django.db.models.query import QuerySet
import copy
"""
1、数据列表页面，定制显示列
    示例一：
    v1.site.register(Model,)  ，默认只显示对象列表
    
    示例二：
    class SubClass(BaseCustom):
        list_display=[]
    v1.site.register(Model,SubClass) 按照list_display 中指定的字段显示
    而这个字段可以 是字符串，也可以是函数，
        如果是字符串需要是数据库的列名，
        如果是函数，需要遵循规则
            def comb(self,obj=None,is_header=False):
                if is_header:
                    return '某列'
                else:
                    return '%s-%s'(obj.username,obj.email)
                    
"""


class BaseCustom(object):
    # list_display = ['id','name']
    list_display = "__all__"
    
    action_list=[]

    filter_list=[]
    
    
    add_or_edit_model_form=None

    def __init__(self,model_class,site):

        self.model_class=model_class
        self.site=site
        self.request=None

        self.app_label=model_class._meta.app_label
        self.model_name=model_class._meta.model_name

        self.list_url=None
    def get_add_or_edit_model_form(self):
        if self.add_or_edit_model_form:
            return self.add_or_edit_model_form
        else:
            from django.forms import ModelForm,widgets,fields

            custome=fields.CharField(widget=widgets.Input())
            _m=type('Meta',(object,),{'model':self.model_class,'fields':"__all__",
                                      'labels':{'username':'用户名','email':'邮箱','ug':'用户组','ur':'角色','name':'用户名'},
                                      'widgets':{'username':widgets.Input(attrs={'class':'form-control'}),
                                                 'email':widgets.Input(attrs={'class':'form-control'}),
                                                 'name':widgets.Input(attrs={'class':'form-control'}),
                                                 'ug':widgets.Select(attrs={'class':'form-control'}),
                                                 'ur':widgets.Select(attrs={'class':'form-control'}),
                                                 },
                                      'error_messages':{'__all__':'不对',
                                                        'username':{'required':'不能为空'},'email':{'required':'输入邮箱'}}
                                      })

            MyModelForm=type('MyModelForm',(ModelForm,),{'Meta':_m})
        # class MyModelForm(ModelForm):
        #     class Meta:
        #         modul=self.model_class
        #         fields="__all__"
        return MyModelForm
    @property
    def urls(self):
        from django.conf.urls import url,include
        info=self.model_class._meta.app_label,self.model_class._meta.model_name
        urlpatterns=[
            url(r'^$',self.changelist_view,name='%s_%s_changelist'%info),
            url(r'^add/$',self.add_view,name='%s_%s_add'%info),
            url(r'^(.+)/delete/$',self.delete_view,name='%s_%s_delete'%info),
            url(r'^(.+)/change/$',self.change_view,name='%s_%s_change'%info),

        ]
        return urlpatterns

    def changelist_view(self,request):
        """
        查看列表
        :param request:
        :return:
        """
        #生成页面上的添加按钮：
        #需要的元素: namespace:app_label ,model_name  reverse
        #self.site.namespace
        #self.model_class._meta.app_label




        from django.http.request import QueryDict

        # print(request.GET.urlencode())

        param_dict=QueryDict(mutable=True)

        if request.GET:
            param_dict['_changelistfilter']=request.GET.urlencode()

        # print(param_dict.urlencode())

        base_add_url=reverse("{2}:{0}_{1}_add".format(self.app_label,self.model_name,self.site.namespace))

        add_url="{0}?{1}".format(base_add_url,param_dict.urlencode())

        self.request=request

        condition={}
        from utils.pager import  PageInfo

        all_count=self.model_class.objects.filter(**condition).count()

        base_page_url=reverse("{2}:{0}_{1}_changelist".format(self.app_label,self.model_name,self.site.namespace))
        import copy
        page_param_dict=copy.deepcopy(request.GET)
        page_param_dict._mutable=True

        page_obj=PageInfo(request.GET.get('page'),all_count,base_page_url,page_param_dict)
        result_list=self.model_class.objects.filter(**condition)[page_obj.start:page_obj.end]


        result_list=self.model_class.objects.all()

 
        ################分页结束##############
        
        ##########Action操作#############
        #get请求，显示 下拉框
        
        action_list=[]

        for item in self.action_list:
            #获取选的
            tpl={'name':item.__name__,'text':item.text}
            action_list.append(tpl)
            
        if request.method=='POST':
            func_name_str=request.POST.get('action')
            
            ret=getattr(self,func_name_str)(request)

            action_page_url = reverse(
                "{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))

            if ret:
                url='{0}?{1}'.format(action_page_url,request.GET.urlencode)
                # print(url)
            return redirect(action_page_url)

        
        ###########组合搜索操作

        filter_list=[]
        
        for option in self.filter_list:
            print(option,'------')
            if option.is_func:
                data_list = option.field_or_func(self,option,request)
            else:
                from django.db.models import ForeignKey, ManyToManyField,OneToOneField
                 #如果是字符串   name ug ,ur   username,获取models.py的类名 以及这个表的字段
                field=self.model_class._meta.get_field(option.field_or_func)
                print(field,'--field-')
                
                if isinstance(field,ForeignKey): #foreignkey的时候，获取到它的关联的表

                    data_list=FilterList(option,field.rel.model.objects.all(),request)

                elif isinstance(field,ManyToManyField):#如果m2m，获取到它的多对多的表。
                    data_list=FilterList(option,field.rel.model.objects.all(),request)

                else:
                    data_list=FilterList(option,field.model.objects.all(),request)

            filter_list.append(data_list)

        context={
            'filter_list': filter_list,
            'result_list':result_list,
            'list_display':self.list_display,
            'display_change':self,
            'add_url':add_url,
            'page_str':page_obj.pager(),
            'action_list':action_list,

        }

        return render(request,'custum/change_list.html',context)

    def add_view(self,request):

        """
        添加数据
        :param request:
        :return:
        """

        # print(request.GET('_changelistfilter'))
        if request.method=='GET':

            model_form_obj=self.get_add_or_edit_model_form()()

            context={
                'form':model_form_obj,
            }
            return render(request, 'custum/add.html', context)
        else:
            model_form_obj=self.get_add_or_edit_model_form()(data=request.POST,files=request.FILES)
            
            if model_form_obj.is_valid():
                obj=model_form_obj.save()
                
                #如果是popup 要返回页面给调用
                popid=request.GET.get('popup')
                print(popid)
                if popid:
                    pk=obj.pk
                    text=str(obj)
                    context={
                        # 'pk':obj.pk,
                        # 'text':str(obj),
                        # 'popid':popid
                        #当数据太多的时候用下面方法封装数据
                        'data_dict':{'pk':obj.pk,'text':str(obj),}
                    }
                    
                    return render(request,'custum/popup_result.html',{'data_dict':{'pk':obj.pk,'text':str(obj),'popid':popid}})
                    
                    
                else:
                    #添加成功，跳转页面
                    #/custom/app01/userinfo/+request.GET.get('_changelistfileter')
                    base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
                    # print(request.GET.get('_changelistfilter'),'0000')
                    self.list_url = "{0}?{1}".format(base_list_url, request.GET.get('_changelistfilter'))
                    return redirect(self.list_url)


            context={
                'form':model_form_obj,
            }
            return render(request, 'custum/add.html', context)


        for item in model_form_obj: #提示显示中文
            # print(item.label) #这样也可以拿到每个INPUT框的中文
            #为多选和下拉框 加一个popup

            print(item.field)


    def delete_view(self,request,pk):
        """
        :param reqeust:
        :return:
        """
        print(request.GET.get('_changelist'),'------')
        info=self.model_class._meta.app_label,self.model_class._meta.model_name
        data="%s_%s_del"%info
        self.model_class.objects.filter(id=pk).delete()
        base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
        self.list_url = "{0}?{1}".format(base_list_url, request.GET.get('_changelistfilter'))
        return redirect(self.list_url)

    def change_view(self,request,pk):

        obj=self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse('id不存在 ')

        if request.method=='GET':
            model_form_obj = self.get_add_or_edit_model_form()(instance=obj)
        else:
            model_form_obj=self.get_add_or_edit_model_form()(data=request.POST,instance=obj) #没有instance 则表示增加，有表示修改

            if model_form_obj.is_valid:
                model_form_obj.save()
            base_list_url = reverse(
                "{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
            self.list_url = "{0}?{1}".format(base_list_url, request.GET.get('_changelistfilter'))
            return redirect(self.list_url)
            
        context={
            'form':model_form_obj
        }
        return render(request,'custum/edit.html',context)


class FilterList(object):
    def __init__(self,option,queryset,request):
        self.option=option
        self.queryset=queryset
        self.path_info=request.path_info
        self.param_dict=copy.deepcopy(request.GET)

    def __iter__(self):
        yield mark_safe("<div class='all-area'>")
        print(self.option.name,'option.name')
        if self.option.name in self.param_dict:
            pop_val = self.param_dict.pop(self.option.name)
            url = "{0}?{1}".format(self.path_info,self.param_dict.urlencode())
            # self.param_dict[self.option.name] = pop_val
            self.param_dict.setlist(self.option.name, pop_val)
            yield mark_safe('<a href="{0}" class="">全部</a>'.format(url))
        else:
            url = "{0}?{1}".format(self.path_info,self.param_dict.urlencode())
            yield mark_safe('<a class="active" href={0}>全部</a>'.format(url))
        yield mark_safe("</div><div class='others-area'>")
        
        for row in self.queryset:
            # print(self.param_dict,'----1--')

            param_dict=copy.deepcopy(self.param_dict)

            pk=str(getattr(row,self.option.val_func_name)() if self.option.val_func_name else int(row.pk))  #这里会执行models.py val_func_name 方法，所以返回的是邮箱或者用户名

            # print(type(pk),pk,'--')#str 如果不用str [['["[\'alith@alex.coma\']", \'abc@qq.com\']', 'alith@alex.coma']]

            text=getattr(row,self.option.text_func_name)() if self.option.text_func_name else str(row)

            active=False
            # print(self.option.name,'self.option.name')
            if self.option.is_multi:
                #username email self.option.name 这里是一个列表#[["['fdsa@qc.com']", 'alith@alex.coma']]
                value_list = param_dict.getlist(self.option.name)
                # print(param_dict.getlist(self.option.name),'param_dict')
                # print('value_list',type(param_dict.getlist(self.option.name)),param_dict.getlist(self.option.name),type(pk),pk,'----')
                
                if pk in value_list: #这里是如果从request.GEt里获取到在之前copy  出来的里面，就把这一次的删除
                    print(pk,type(pk),'value_list',value_list)

                    value_list.remove(pk)
                    param_dict.setlist(self.option.name,value_list)
                    print(value_list,'=')

                    active=True

                    """
                    value_list [['abc@qq.com']] alith@alex.coma
                    value_list [['abc@qq.com']] abc@qq.com
                    value_list [['abc@qq.com']] xian@xian.com
                    value_list [['abc@qq.com']] fdsa@qc.com
                    """
                    # print(value_list,'=-=-=')

                else:
                    param_dict.appendlist(self.option.name,pk)#custom/app02/userinfo/?email=%5B%27alith%40alex.coma%27%5D&email=abc%40qq.com


            else:
                value_list=param_dict.getlist(self.option.name)
                if pk in value_list:#如果不是多选 ，就直接把 深拷贝出来的option.name 重新赋值
                    active=True
                param_dict[self.option.name]=pk  #重新赋值，因为不是多选
            
            url='{0}?{1}'.format(self.path_info,param_dict.urlencode())

            if active:
                tpl="<a href='{0}' class='active'>{1}</a>".format(url,text)
            else:
                tpl="<a href='{0}'>{1}</a>".format(url,text)

            yield mark_safe(tpl)

        yield mark_safe('</div>')

class FilterOption(object):
    def __init__(self, field_or_func, is_multi=False, text_func_name=None, val_func_name=None):
        """
        :param field: 字段名称或函数
        :param is_multi: 是否支持多选
        :param text_func_name: 在Model中定义函数，显示文本名称，默认使用 str(对象)
        :param val_func_name:  在Model中定义函数，显示文本名称，默认使用 对象.pk
        """
        self.field_or_func = field_or_func
        self.is_multi = is_multi
        self.text_func_name = text_func_name
        self.val_func_name = val_func_name

    @property
    def is_func(self):
        if isinstance(self.field_or_func, FunctionType):
            return True

    @property
    def name(self):
        if self.is_func:
            return self.field_or_func.__name__
        else:
            return self.field_or_func


class Custom(object):
    
    def __init__(self):
        
        self._registry={}
        
        self.namespace='custom'
        
        self.app_name='custom'

    def register(self,model_class,BaseClass=BaseCustom): #注册方法如admin.site.register(models.Role) model_clss类也就是表的名称，
        """_registry
        {
          _registry[model.Role]:obj
        }
        """

        self._registry[model_class]=BaseClass(model_class,self)
        print(self._registry,self,'----')
        """
        app名称models类名：BaseCustom 类封装了 app名称models类名,Custum对象
        {<class 'app02.models.Role'>: <app03.service.v1.BaseCustom object at 0x106149c18>, 
        <class 'app01.models.App02Userinfo'>: <app03.service.v1.BaseCustom object at 0x1061499b0>}
        {<class 'app02.models.Role'>: <app03.service.v1.BaseCustom object at 0x106149c18>, 
        <class 'app01.models.App02Userinfo'>: <app03.service.v1.BaseCustom object at 0x1061499b0>,
         <class 'app02.models.test1'>: <app03.service.v1.BaseCustom object at 0x106149940>}
         
        """


    def get_urls(self):
        from django.conf.urls import url,include
        ret=[
            # url(r'login/',self.login,name='login'),
            # url(r'logout/',self.logout,name='logout'),

        ]

        for model_cls,admin_obj in self._registry.items():
            print(model_cls,model_cls._meta.app_label,'---',model_cls._meta.model_name)
                            #app名字                          #模块名字
            app_labe=model_cls._meta.app_label
            model_name=model_cls._meta.model_name
            ret.append(url(r'%s/%s/'%(app_labe,model_name), include(admin_obj.urls))) #反生成,当每个APP的URL进来时，每个APP都 有
            #自己的增删改查。

        return ret

    def login(self,request):
        return HttpResponse('login')
    def logout(self,request):
        return HttpResponse('logout')

    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.namespace


site=Custom()
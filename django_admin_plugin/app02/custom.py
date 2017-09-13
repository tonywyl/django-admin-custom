print('cusmtom app02')


from app03.service import v1
from app02 import models
from django.utils.safestring import mark_safe
from django.urls import reverse
from app03.service.v1 import FilterOption
from app03.service.v1 import FilterList
class display_oprate(v1.BaseCustom):

    def func(self, obj=None,is_header=False):
        if is_header:
            return mark_safe('<th>操作</th>')
        else:
            """
            显示操作字段
            """
            from django.http.request import QueryDict
            param_dict = QueryDict(mutable=True)

            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()
                param_dict['_delete']=self.request.GET.urlencode()

            base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label, self.model_name, self.site.namespace),args=(obj.pk,))
            base_del_url = reverse("{2}:{0}_{1}_delete".format(self.app_label, self.model_name, self.site.namespace),args=(obj.pk,))
            # reverse{namespace:}
            edit_url="{0}?{1}".format(base_edit_url,param_dict.urlencode())
            del_url="{0}?{1}".format(base_del_url,param_dict.urlencode())
            return mark_safe("<td><a href='{0}' class='btn btn-default'>编辑</a>&nbsp;&nbsp;<a href='{1}' class='btn btn-default'>删除</a></td>".format(edit_url,del_url))

    def checkbox(self, obj=None,is_header=False):
        if is_header:
            return mark_safe('选项')
            # return mark_safe("<input type='checkbox'/>")
        else:
            tag = '<input type="checkbox" value="{0}" />'.format(obj.pk)
            return mark_safe(tag)

    def comb(self,obj=None,is_header=False):
        if is_header:
            return mark_safe('地域')
        else:
            return "%s-%s"%(obj.username,obj.email)

    list_display = [checkbox, 'id', 'username', 'email', comb, func]

    def initial(self,request):
        pk_list=request.POST.getlist('pk')
        
        models.UserInfo.objects.filter(pk__in=pk_list).update(username='中南海第十军区五团')
        return True
    initial.text='初始化'

    def multi_del(self,request):
        pass
    multi_del.text='批量删除1'

    action_list = [initial,multi_del]

    def username(self,option,request):
        queryset=models.UserInfo.objects.filter(id__gt=1)
        return FilterList(option,queryset,request)

    def email(self,option,request):
        queryset = models.UserInfo.objects.filter(id__gt=1)
        return FilterList(option, queryset, request)

    filter_list = [
        FilterOption(username,False,text_func_name='text_username',val_func_name='value_username'),
        FilterOption(email,True,text_func_name='text_email',val_func_name='value_email'),
        FilterOption('ug',True,),
        FilterOption('ur',True,),
    ]



class Display_userinfo(v1.BaseCustom):
    list_display=['id','username','email']

class Display_Role(v1.BaseCustom):
    def func(self, obj=None,is_header=False):
        """
        显示操作字段
        """
        if is_header:
            return mark_safe('<th>操作</th>')
        else:
            """
            显示操作字段
            """
            from django.http.request import QueryDict
            param_dict = QueryDict(mutable=True)

            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()
                param_dict['_delete']=self.request.GET.urlencode()

            base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label, self.model_name, self.site.namespace),args=(obj.pk,))
            base_del_url = reverse("{2}:{0}_{1}_delete".format(self.app_label, self.model_name, self.site.namespace),args=(obj.pk,))
            # reverse{namespace:}
            edit_url="{0}?{1}".format(base_edit_url,param_dict.urlencode())
            del_url="{0}?{1}".format(base_del_url,param_dict.urlencode())
            return mark_safe("<td><a href='{0}' class='btn btn-default'>编辑</a>&nbsp;&nbsp;<a href='{1}' class='btn btn-default'>删除</a></td>".format(edit_url,del_url))

    def checkbox(self, obj=None,is_header=False):
        if is_header:
            return mark_safe("<input type='checkbox'/>")
        else:
            tag = '<input type="checkbox" value="{0}" />'.format(obj.pk)
            return mark_safe(tag)

    list_display = [checkbox, 'id', 'name', func]

class Display_test1(v1.BaseCustom):
    def func(self,obj=None,is_header=False):
        """
        显示操作字段
        """
        if is_header:
            return mark_safe('<th>操作</th>')
        else:
            """
            显示操作字段
            """
            from django.http.request import QueryDict
            param_dict = QueryDict(mutable=True)

            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()
                param_dict['_delete']=self.request.GET.urlencode()

            base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label, self.model_name, self.site.namespace),args=(obj.pk,))
            base_del_url = reverse("{2}:{0}_{1}_delete".format(self.app_label, self.model_name, self.site.namespace),args=(obj.pk,))
            # reverse{namespace:}
            edit_url="{0}?{1}".format(base_edit_url,param_dict.urlencode())
            del_url="{0}?{1}".format(base_del_url,param_dict.urlencode())
            return mark_safe("<td><a href='{0}' class='btn btn-default'>编辑</a>&nbsp;&nbsp;<a href='{1}' class='btn btn-default'>删除</a></td>".format(edit_url,del_url))
    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return mark_safe("<input type='checkbox'/>")
        else:
            tag = '<input type="checkbox" value="{0}" />'.format(obj.pk)
            return mark_safe(tag)

    list_display = [checkbox,'id','title',func]

class Display_group(v1.BaseCustom):
    def func(self,obj=None,is_header=False):
        """
        显示操作字段
        """
        if is_header:
            return '操作'
        else:
            """
            显示操作字段
            """
            from django.http.request import QueryDict
            param_dict = QueryDict(mutable=True)

            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()

            base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label, self.model_name, self.site.namespace),
                                    args=(obj.pk,))
            # reverse{namespace:}
            edit_url = "{0}?{1}".format(base_edit_url, param_dict.urlencode())
            return mark_safe("<a href='{0}'>编辑</a>".format(edit_url))

    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return mark_safe("<input type='checkbox'/>")
        else:
            tag = '<input type="checkbox" value="{0}" />'.format(obj.pk)
            return mark_safe(tag)


    list_display = [checkbox,'id','title',func]

    def initial(self,request):
        """

        :param request:
        :return:
        """
        pk_list=request.POST.getlist('pk')
        models.UserInfo.objects.filter(pk__in=pk_list).update(name='中南海第九师五旅')
        return True
    initial.text='全部换成 中南海第九师五旅'

    def multi_del(self,request):
        """

        :param request:
        :return:
        """
    multi_del.text='批量删除'
    action_list = [initial,multi_del]
    from app03.service.v1 import FilterOption
    #text_func_name 写了这个就models.py就不找自己的__str__, 没写这个就默认找__str__,所以 在models.py写一个text_username
    filter_list = [
        FilterOption('username',False,text_func_name='text_username',val_func_name='value_username'),
        FilterOption('email',False),
        FilterOption('ug',False),
        FilterOption('ur',False),
    ]

v1.site.register(models.UserInfo,display_oprate)

v1.site.register(models.Role,Display_Role)
v1.site.register(models.test1,Display_test1)
v1.site.register(models.UserGroup,Display_group)
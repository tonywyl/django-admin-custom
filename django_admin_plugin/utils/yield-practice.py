# class compute:
#     def __init__(self,option,data_list):
#         self.option=option
#         self.data_list=data_list
#
#     def __iter__(self):
#         yield 'all:'
#         for item in self.data_list:
#             yield item
#
#
# class apple:
#     def __init__(self,name,year):
#         self.name=name
#         self.year=year
#
#     def show(self):
#         print(self.name)
#
#
# obj_list=[
#     compute(apple('Mac',2011,),[' apple iphone','Macpro']),
#     compute(apple('lenevo',2004,),[' lenevo phone','lenevo compute']),
#
#
# ]
# obj1=compute(apple('Mac',2011,),['apple iphone','Macpro'])
#
#
#
# print(obj1)
# for i in obj_list:
#     for item in i:
#         print(item,end='')
#     else:
#         print('')


class Main1:
    def __init__(self,option,data_list):
        self.option=option
        self.data_list=data_list

    def __iter__(self):
        yield '全部：'
        for i in self.data_list:
            yield "<a href='{0}'>{1}</a>".format(i,i+str(self.option.age))


class Sub:
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def show(self):
        print(self.name)


data_list=[
    Main1(Sub('互联网: ',20),['百度','搜狗','google','tecent']),
    Main1(Sub('汽车: ',20),['大众','奥迪','宝马','奔驰']),

]

for obj in data_list:
    for item in obj:
        print(item,end=' ')
    else:
        print('')









































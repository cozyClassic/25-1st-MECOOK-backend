from django.http.response import HttpResponse
from django.shortcuts   import render
from django.http        import JsonResponse
from product.models     import Categories, Products, Hashtags, Menus
from django.views       import View

# Create your views here.


class MenuList(View) :
    def get(self,request) :
        data = list(Menus.objects.all().values_list())
        return JsonResponse({"result" : data})
class CategoryList(View) :
    def get(self,request) :
        data = list(Categories.objects.all().values_list())
        return JsonResponse({"result" : data})
    
class ProductList(View) :
    def get(self,request) :
        data = list(Products.objects.all().values_list())
        return JsonResponse({"result" : data})
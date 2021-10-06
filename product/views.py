from django.http        import JsonResponse
from django.http.response import HttpResponse
from product.models     import Categories, Products, Hashtags, Menus, ProductAndHashtag
from django.views       import View

# Create your views here.

class CategoryList(View) :
    def get(self,request) :
        data = list(Categories.objects.all().values_list())
        return JsonResponse({"result" : data})

class ProductList(View) :
    def get(self,request) :
        data = list(Products.objects.all().values_list())
        return JsonResponse({"result" : data})


class MenuList(View) :
    def get(self,request) :
        data = list(Menus.objects.all().values_list())
        return JsonResponse({"result" : data})


class MenuByCategory(View) :
    def get(self,request,category_id) :
        data = list(Products.objects.filter(category_id=category_id).values_list())
        return JsonResponse({"result" : data})

# 카테고리, 메뉴이름, 조리시간, 몇인분인지, 좋아요 개수
class ListByCategory(View) :
    def get(self,request,category_id) :
        data = Products.objects.filter(category_id=category_id)
        category_name = Categories.objects.get(id=category_id).name
        result = []
        for i in data :
            result.append([category_name, i.name, i.cook_time, i.servings_g_people, 0])

        return JsonResponse({
            "result" : result
        })


#조리시간, 몇인분인지, 카테고리, 좋아요 개수,  해시태그

class DetailByProduct(View) :
    def get(self,reqeust,product_id) :
        products_query = Products.objects.get(id=product_id)
        category_name = Categories.objects.get(id=products_query.category_id).name
        result = []
        hashtags = []
        hash_numbers = ProductAndHashtag.objects.filter(product_id=product_id).values_list()
        for i in hash_numbers :
            hashtags.append(i[2])

        result.append([products_query.cook_time, products_query.servings_g_people, category_name, 0])
        result.append(hashtags)
        
        return JsonResponse({
            "result" : result
        })
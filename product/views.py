from django.http.response import HttpResponse
from django.shortcuts   import render
from django.http        import JsonResponse
from product.models     import Categories, Products, Hashtags
from django.views       import View

# Create your views here.

class CategoryList(View) :
    def get(self,request) :
        data = Categories.objects.all()
        result = []
        for i in data :
            result.append(i.name)

        return JsonResponse({"result" : result})

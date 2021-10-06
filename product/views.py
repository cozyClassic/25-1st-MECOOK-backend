from django.shortcuts   import render
from django.http        import JsonResponse
from product.models     import Categories, Products, Hashtags
from django.views       import View

# Create your views here.

class CategoryList(View) :
    def get(self,request) :
        data = Categories.objects.all()
        return JsonResponse(data)


from django.http        import JsonResponse
from django.http.response import HttpResponse
from product.models     import Categories, Products, Hashtags, Menus, ProductsHashtag, ProductsMainImages, ProductDetailAttrs
from likes.models       import Like
from django.views       import View
from django.db.models   import Q, Count

# Create your views here.


class MenuRaw(View) :
    def get(self,request) :
        data = ["메뉴ID, 메뉴명"]
        data.append(list(Menus.objects.all().values_list()))

        return JsonResponse({"result" : data})


class CategoryRaw(View) :
    def get(self,request) :
        data = ["카테고리ID", "카테고리명", "메뉴ID"]
        data.append(list(Categories.objects.all().values_list()))
        
        return JsonResponse({"result" : data})


class ProductRaw(View) :
    def get(self,request) :
        data = [["상품ID", "상품명", "카테고리ID", "원래가격", "할인가격", "이벤트가격", "용량/인분", "조리시간","메인텍스트",
        "썸네일_마우스오버","썸네일_마우스아웃","상세페이지","진열순위","판매자ID","생성일","수정일","삭제일"]]
        data.append(list(Products.objects.all().values_list()))

        return JsonResponse({"result" : data})


class CategoryByMenu(View) :
    def get(self,reqeust,menu_id) :
        data = ["카테고리ID", "카테고리명", "메뉴ID"]
        data.append(list(Categories.objects.filter(menu_id=menu_id).values_list()))

        return JsonResponse({"result" : data})


class ProductByCategory(View) :
    def get(self,request,category_id) :
        data = [["상품ID", "상품명", "카테고리ID", "원래가격", "할인가격", "이벤트가격", "용량/인분", "조리시간","메인텍스트",
        "썸네일_마우스오버","썸네일_마우스아웃","상세페이지","진열순위","판매자ID","생성일","수정일","삭제일"]]
        data.append(list(Products.objects.filter(category_id=category_id).values_list()))

        return JsonResponse({"result" : data})


# 카테고리, 메뉴이름, 조리시간, 몇인분인지, 좋아요 개수
class ListByCategory(View) :
    def get(self,request,category_id) :
        data = Products.objects.filter(category_id=category_id).select_related('category')
        result = []
        for i in data :
            result.append({
                "id"            : i.id,
                "mainImage"     : i.thumbnail_out_url,
                "subImage"      : i.thumbnail_over_url,
                "category"      : i.category.name,
                "name"          : i.name,
                "cookingTime"   : i.cook_time,
                "serving"       : i.servings_g_people,
                "like"          : 0,
                }
            )

        return JsonResponse({
            "result" : [result]
        })


# 제품명, 조리시간, 몇인분인지, 카테고리, 좋아요 개수,  해시태그
class DetailByProduct(View) :
    def get(self,reqeust,product_id) :
        products = Products.objects.select_related('category'
        ).prefetch_related('product_main_images'
        ).prefetch_related('products_hashtag'
        ).prefetch_related('product_detail_attrs'
        ).get(id=product_id) #1
        hash_numbers = [x[0] for x in list(products.products_hashtag.values_list('hashtag_id'))]
        detail = [{
            "text" : i.text,
            "image_url" : i.image_url,
            "priority" : i.priority,
            } for i in products.product_detail_attrs.filter(product_id=product_id)]
        
        hash_names = [x[0] for x in list(Hashtags.objects.filter(id__in=hash_numbers).values_list('name'))]

        result = {
            "image"         : products.product_main_images.values("main_image_url").get(product_id=product_id)["main_image_url"],
            "category"      : products.category.name, #1
            "name"          : products.name,
            "hashtag"       : hash_names
        }
        
        return JsonResponse({
            "result" : [result],
            "detail" : detail
        })


class TestView(View) :
    def get(self,reqeust,product_id) :
        products = Products.objects.select_related('category'
        ).prefetch_related('product_main_images'
        ).prefetch_related('products_hashtag'
        ).prefetch_related('product_detail_attrs'
        ).get(id=product_id) #1

        likes = Like.objects.filter(product_id=product_id).count()
        

        hash_numbers = [x[0] for x in list(products.products_hashtag.values_list('hashtag_id'))]
        detail = [{
            "text" : i.text,
            "image_url" : i.image_url,
            "priority" : i.priority,
            } for i in products.product_detail_attrs.filter(product_id=product_id)]
        
        hash_names = [x[0] for x in list(Hashtags.objects.filter(id__in=hash_numbers).values_list('name'))]

        result = {
            "image"         : products.product_main_images.values("main_image_url").get(product_id=product_id)["main_image_url"],
            "category"      : products.category.name, #1
            "name"          : products.name,
            "likes"         : likes,
            "hashtag"       : hash_names
        }
        
        return JsonResponse({
            "result" : [result],
            "detail" : detail
        })


class ProductDetailComponent(View) :
    def get(self,request,product_id) :
        ProductDetailAttrs.objects.filter(product_id=product_id)
        return JsonResponse({"result" : ["HI!"]})
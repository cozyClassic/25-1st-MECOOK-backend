from django.http        import JsonResponse
from product.models     import Categories, Products, Hashtags, Menus, ProductAndHashtag, ProductsMainImages
from django.views       import View
from django.db.models   import Q

# Create your views here.


class MenuList(View) :
    def get(self,request) :
        data = list(Menus.objects.all().values_list())
        return JsonResponse({"result" : data})
class CategoryList(View) :
    def get(self,request) :
        data = ["카테고리ID", "카테고리명", "메뉴ID"]
        data.append(list(Categories.objects.all().values_list()))
        
        return JsonResponse({"result" : data})

class ProductList(View) :
    def get(self,request) :
        data = [["상품ID", "상품명", "카테고리ID", "원래가격", "할인가격", "이벤트가격", "용량/인분", "조리시간","메인텍스트","썸네일_마우스오버","썸네일_마우스아웃","상세페이지","진열순위","판매자ID","생성일","수정일","삭제일"]]
        data.append(list(Products.objects.all().values_list()))
        return JsonResponse({"result" : data})


class MenuList(View) :
    def get(self,request) :
        data = ["메뉴ID, 메뉴명"]
        data.append(list(Menus.objects.all().values_list()))
        return JsonResponse({"result" : data})


class MenuByCategory(View) :
    def get(self,request,category_id) :
        data = [["상품ID", "상품명", "카테고리ID", "원래가격", "할인가격", "이벤트가격", "용량/인분", "조리시간","메인텍스트","썸네일_마우스오버","썸네일_마우스아웃","상세페이지","진열순위","판매자ID","생성일","수정일","삭제일"]]
        data.append(list(Products.objects.filter(category_id=category_id).values_list()))
        return JsonResponse({"result" : data})

# 카테고리, 메뉴이름, 조리시간, 몇인분인지, 좋아요 개수
class ListByCategory(View) :
    def get(self,request,category_id) :
        data = Products.objects.filter(category_id=category_id)
        category_name = Categories.objects.get(id=category_id).name
        result = []
        for i in data :
            result.append({
                "mainImage" : i.thumbnail_out_url,
                "subImage" : i.thumbnail_over_url,
                "category" : category_name,
                "name" : i.name,
                "cookingTime" : i.cook_time,
                "serving" : i.servings_g_people,
                "like" : 0,
                }
            )

        return JsonResponse({
            "result" : [result]
        })


# 제품명, 조리시간, 몇인분인지, 카테고리, 좋아요 개수,  해시태그

class DetailByProduct(View) :
    def get(self,reqeust,product_id) :
        products_query = Products.objects.get(id=product_id)
        category_name = Categories.objects.get(id=products_query.category_id).name
        hashtag_ids = []
        hash_numbers = ProductAndHashtag.objects.filter(product_id=product_id).values_list()
        image_url_main = ProductsMainImages.objects.get(product_id=product_id).main_image_url
        for i in hash_numbers :
            hashtag_ids.append(i[2])
        
        hashtag_names = []
        for j in hashtag_ids :
            hashtag_names.append(Hashtags.objects.get(id=j).name)
        

        result = {
            "image" : image_url_main,
            "category" : category_name,
            "name" : products_query.name,
            "cookingTime" : products_query.cook_time,
            "serving" : products_query.servings_g_people,
            "hashtag" : hashtag_names
        }
        
        return JsonResponse({
            "result" : [result],
        })

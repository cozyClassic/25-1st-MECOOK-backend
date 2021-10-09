from django.http        import JsonResponse
from django.http.response import HttpResponse
from product.models     import Categories, Products, Hashtags, Menus, ProductsHashtag, ProductsMainImages, ProductDetailAttrs
from likes.models       import Like
from django.views       import View
from django.db.models   import Q, Count
from users.utils        import login_decorator
from collections        import Counter
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
        
        # AccessToken이 있는 경우에만 체크를 하기 위해 데코레이터를 내부로 호출함
        @login_decorator
        def get_user_id(self,request) :
            return request.user.id

        data = Products.objects.select_related('category').filter(category_id=category_id)
        product_lists = []
        for i in data :
            product_lists.append(i.id)

        # 좋아요 테이블에서, 우리가 보여줄 목록에 있는 상품이 들어있는 모든 좋아요 데이터를 가져와서 Counter 사용
        likes = list(Like.objects.filter(product_id__in=product_lists).values_list())
        likes_list = Counter([x[1] for x in likes])
        like_boolean = []

        # AccessToken이 있는 경우에, Like 테이블에서 해당 사용자가 좋아요를 누른 상품 리스트를 찾음.
        if 'Authorization' in request.headers :
            user_id = get_user_id(self,request)
            like_boolean = [x[2] for x in list(Like.objects.filter(user_id =user_id, product_id__in=product_lists).values_list())]

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
                "like"          : likes_list[i.id],
                "this_user_like": int(i.id in like_boolean),
                "product_lists" : product_lists,                
                }
            )
        

        return JsonResponse({
            "result" : result
        })


# 제품명, 조리시간, 몇인분인지, 카테고리, 좋아요 개수,  해시태그
class DetailByProduct(View) :
    def get(self,request,product_id) :
        
        @login_decorator
        def get_user_id(self,request) :
            return request.user.id
        
        # product 테이블의 ID를 foreignKEY로 사용하는 테이블들을 한번에 가져오기 위해 prefetch_realated사용
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
        
        if 'Authorization' in request.headers :
            user_id = get_user_id(self,request)
            like_boolean = Like.objects.filter(product_id=product_id, user_id =user_id).exists()
            result["this_user_like"] = int(like_boolean)

        return JsonResponse({
            "result" : [result],
            "detail" : detail
        })


# 카테고리 기준으로 상품리스트 반환하는것과 거의 동일하지만, 카테고리 기준이 아닌 좋아요가 높은 숫자의 상품을 반환하도록 되어 있음.
class ListByLike(View) :
    def get(self,request,*args) :

        @login_decorator
        def get_user_id(self,request) :
            return request.user.id

        # 좋아요에서 가장 숫자가 높은 친구들 찾기.
        likes = [x["product_id"] for x in list(Like.objects.all().values('product_id'))]
        top6 = [x[0] for x in sorted(list(Counter(likes).items()), key=lambda x : x[1], reverse=True)[:6]]
        likes_lists = [x[1] for x in sorted(list(Counter(likes).items()), key=lambda x : x[1], reverse=True)[:6]]
        product_lists = Products.objects.filter(id__in =top6)
        
        
        idx = 0
        like_boolean = []
        if 'Authorization' in request.headers :
            user_id = get_user_id(self,request)
            like_boolean = [x[2] for x in list(Like.objects.filter(user_id =user_id, product_id__in=product_lists).values_list())]

        result = []
        for i in product_lists :
            result.append({
                "id"            : i.id,
                "mainImage"     : i.thumbnail_out_url,
                "subImage"      : i.thumbnail_over_url,
                "category"      : i.category.name,
                "name"          : i.name,
                "cookingTime"   : i.cook_time,
                "serving"       : i.servings_g_people,
                "like"          : likes_lists[idx],
                "this_user_like": int(i.id in like_boolean)
                }
            )
            idx+=1
        

        return JsonResponse({
            "result" : result
        })



#
class TestView(View) :
    def get(self,request,category_id) :

        @login_decorator
        def get_user_id(self,request) :
            return request.user.id

        data = Products.objects.select_related('category').filter(category_id=category_id)
        product_lists = []
        for i in data :
            product_lists.append(i.id)
        likes = list(Like.objects.filter(product_id__in=product_lists).values_list())
        likes_list = Counter([x[1] for x in likes])
        like_boolean = []
        if 'Authorization' in request.headers :
            user_id = get_user_id(self,request)
            like_boolean = [x[2] for x in list(Like.objects.filter(user_id =user_id, product_id__in=product_lists).values_list())]

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
                "like"          : likes_list[i.id],
                "this_user_like": int(i.id in like_boolean),
                "product_lists" : product_lists,                
                }
            ) 
        

        return JsonResponse({
            "result" : result
        })

"""
class LoginSample(View) :
    def get(self,request,product_id) :
        @login_decorator
        def user_id(self,request) :
            return request.user.id

        if 'Authorization' in request.headers :
            result = user_id(self,request)
            return HttpResponse(result)
        else : 
            return HttpResponse("No JWT")
"""
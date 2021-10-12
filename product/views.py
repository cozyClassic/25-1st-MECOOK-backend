from django.http        import JsonResponse
from product.models     import Products, Hashtags
from likes.models       import Like
from django.views       import View
from users.utils        import login_decorator
from collections        import Counter


class ListByCategory(View) :
    def get(self,request,category_id) :

        @login_decorator
        def get_user_id(self,request) :
            return request.user.id

        data            = Products.objects.select_related('category').filter(category_id=category_id).prefetch_related('like_by_product')
        product_lists   = [x.id for x in data]
        likes           = Like.objects.filter(product_id__in=product_lists).all()
        likes_list      = Counter([x.product_id for x in likes.all()])
        like_boolean    = []

        if 'Authorization' in request.headers :
            user_id         = get_user_id(self,request)
            like_boolean    = [like.product_id for like in likes.all() if like.user_id==user_id]

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
                }
            )
        
        return JsonResponse({
            "result" : result
        })


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
        ).prefetch_related('like_by_product'
        ).filter(id=product_id)[0]

        likes = products.like_by_product.count()
        
        hash_numbers    = [x['hashtag_id'] for x in list(products.products_hashtag.values('hashtag_id'))]
        hash_names      = [x['name'] for x in list(Hashtags.objects.filter(id__in=hash_numbers).values('name'))]
        detail = [{
            "text"      : i.text,
            "image_url" : i.image_url,
            "priority"  : i.priority,
            } for i in [attr for attr in products.product_detail_attrs.all() if attr.product_id==product_id]]
        

        result = {
            "image"     : products.product_main_images.get(product_id=product_id).main_image_url,
            "category"  : products.category.name,
            "name"      : products.name,
            "likes"     : likes,
            "hashtag"   : hash_names
        }
        
        if 'Authorization' in request.headers :
            user_id                     = get_user_id(self,request)
            like_boolean                = bool([like for like in products.like_by_product.all() if like.user_id==user_id])
            result["this_user_like"]    = int(like_boolean)

        return JsonResponse({
            "result" : [result],
            "detail" : detail
        })


# 카테고리 기준으로 상품리스트 반환하는것과 거의 동일하지만, 카테고리 기준이 아닌 좋아요가 높은 숫자의 상품을 반환하도록 되어 있음.
class ListByLike(View) :
    def get(self,request,**kwrgs) :

        @login_decorator
        def get_user_id(self,request) :
            return request.user.id

        likes           = Like.objects.all()
        likes2          = sorted(list(Counter([like.product_id for like in likes]).items()), key=lambda x : x[1], reverse=True)[:6]
        product_lists   = Products.objects.filter(id__in=[x[0] for x in likes2])
        idx             = 0
        like_boolean    = []
        result          = []

        if 'Authorization' in request.headers :
            user_id         = get_user_id(self,request)
            like_boolean    = [like.product_id for like in likes if like.user_id == user_id and like.product_id in product_lists]

        
        for i in product_lists :
            result.append({
                "id"            : i.id,
                "name"          : i.name,
                "like"          : likes2[idx][1],
                "this_user_like": int(i.id in like_boolean)
                }
            )
            idx+=1
        

        return JsonResponse({
            "result" : result
        })


class testView(View) :
    def get(self,request,**kwrgs) :

        @login_decorator
        def get_user_id(self,request) :
            return request.user.id

        likes           = Like.objects.all()
        likes2          = sorted(list(Counter([like.product_id for like in likes]).items()), key=lambda x : x[1], reverse=True)[:6]
        product_lists   = Products.objects.filter(id__in=[x[0] for x in likes2])
        idx             = 0
        like_boolean    = []
        result          = []

        if 'Authorization' in request.headers :
            user_id         = get_user_id(self,request)
            like_boolean    = [like.product_id for like in likes if like.user_id == user_id and like.product_id in product_lists]

        
        for i in product_lists :
            result.append({
                "id"            : i.id,
                "name"          : i.name,
                "like"          : likes2[idx][1],
                "this_user_like": int(i.id in like_boolean)
                }
            )
            idx+=1
        

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

list = [(1,3),(4,5),(6,7)]
list2 = [1,4,6]
list = [3,5,7]

for x in list :
    a,b = x

list2 = [x[0] for x in list]
list3 = [x[1] for x in list]
"""
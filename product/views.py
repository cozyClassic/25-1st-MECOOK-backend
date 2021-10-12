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
        ).get(id=product_id)

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
    def get(self,request) :

        @login_decorator
        def get_user_id(self,request) :
            return request.user.id

        likes_query     = Like.objects.all()
        likes_list      = sorted(list(Counter([like.product_id for like in likes_query]).items()), key=lambda x : x[1], reverse=True)[:6]
        product_lists   = Products.objects.filter(id__in=[x[0] for x in likes_list])
        idx             = 0
        like_boolean    = []
        result          = []

        if 'Authorization' in request.headers :
            user_id         = get_user_id(self,request)
            like_boolean    = [like.product_id for like in likes_query if like.user_id == user_id and like.product_id in product_lists]

        
        for i in product_lists :
            result.append({
                "id"            : i.id,
                "name"          : i.name,
                "like"          : likes_list[idx][1],
                "this_user_like": int(i.id in like_boolean)
                }
            )
            idx+=1
        

        return JsonResponse({
            "result" : result
        })

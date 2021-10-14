import json
import re
from django.http        import JsonResponse
from django.http.response import HttpResponse
from product.models     import Products, Hashtags, ProductsHashtag, ProductDetailAttrs
from likes.models       import Like
from django.views       import View
from users.utils        import login_decorator
from collections        import Counter
from django.db          import connection
from django.db.models   import Q



class ListByCategory(View) :
    def get(self,request,category_id) :

        @login_decorator
        def get_user_id(self,request) :
            return request.user.id

        data            = Products.objects.select_related('category').filter(category_id=category_id).prefetch_related('like_by_product')
        product_lists   = [x.id for x in data]
        likes           = Like.objects.filter(product_id__in=product_lists)
        likes_list      = Counter([x.product_id for x in likes])
        like_boolean    = []

        if 'Authorization' in request.headers :
            user_id         = get_user_id(self,request)
            like_boolean    = [like.product_id for like in likes if like.user_id==user_id]

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
        }, status=200)


class DetailByProduct(View) :
    def get(self,request,product_id) :
        
        @login_decorator
        def get_user_id(self,request) :
            return request.user.id
        
        # product 테이블의 ID를 foreignKEY로 사용하는 테이블들을 한번에 가져오기 위해 prefetch_realated사용
        products = Products.objects.select_related('category'
        ).prefetch_related('product_main_images'
        ).prefetch_related('products_by_hashtag'
        ).prefetch_related('product_detail_attrs'
        ).prefetch_related('like_by_product'
        ).get(id=product_id)

        likes = products.like_by_product.count()
        
        hash_numbers    = [x['hashtag_id'] for x in list(products.products_by_hashtag.values('hashtag_id'))]
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
        }, status=200)


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
        }, status=200)


class ListByKeyword(View) :
    def get(self,request) :
        return HttpResponse("URL ALIVE")
    
    def post(self,request) :
        @login_decorator
        def get_user_id(self,request) :
            return request.user.id

        if not "keyword" in json.loads(request.body) :
            return JsonResponse({
                'message': 'keyword does not exist'
            }, status=200)
        search_words = json.loads(request.body)["keyword"]
        print(search_words)
        products_all_query = Products.objects.all()
        hashtags_all_query = Hashtags.objects.all()
        product_id_set = set()
        # product 에서 찾기.
        for key in search_words :
            products_id_list = [product.id for product in products_all_query if bool(re.search(key,product.name))]
            for id in products_id_list :
                product_id_set.add(id)

        # 해시태그로 찾기.
        for key in search_words :
            hashtag_id_list = [tag.id for tag in hashtags_all_query if bool(re.search(key, tag.name))]
            products_id_list = [mid.product_id for mid in ProductsHashtag.objects.filter(hashtag_id__in= hashtag_id_list)]
            for id in products_id_list :
                product_id_set.add(id)

        data            = Products.objects.select_related('category').filter(id__in=list(product_id_set)).prefetch_related('like_by_product')
        
        likes           = Like.objects.filter(product_id__in=list(product_id_set)).all()
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
        }, status=200)

class testView(View) :
    def get(self,request) :       
        # 프론트에 보낼 데이터 짝맞추기 용
        keyword_dicts = {
            'id'            : 'id',
            'name'          : 'name',
            'thumbImg'      : 'thumbnail_out_url',
            'thumbImgHover' : 'thumbnail_over_url', 
            'cookingTime'   : 'cook_time', 
            'serving'       : 'servings_g_people', 
            'category'      : 'category__name',
            'priority'      : 'priority'
            }

        product_queryset= Products.objects.select_related('category').values(*[keyword_dicts[key] for key in keyword_dicts])
        key_querys      = request.GET
        result          = []

        # url_query_parameters = {"product","category","search", "sort","start","limit",,"detail"}
        if "product" in key_querys :
            product_queryset = product_queryset.filter(id=key_querys["product"])

        if "category" in key_querys :
            product_queryset = product_queryset.filter(category_id=key_querys["category"])
        
        if "search" in key_querys :
            q_hashtag = Q()
            q_produt  = Q()
            hash_names_query = ProductsHashtag.objects.select_related('hashtag').values('hashtag__name','product_id')

            for keyword in request.GET.getlist("search") :
                q_hashtag.add(Q(hashtag__name__icontains=keyword), q_hashtag.OR)
                q_produt.add(Q(name__icontains=keyword), q_produt.OR)
                
            hashtag_id_list = [mid["product_id"] for mid in hash_names_query.filter(q_hashtag)]   
            q_produt.add(Q(id__in=hashtag_id_list), q_produt.OR)
            product_queryset = product_queryset.filter(q_produt)
                
        if "sort" in key_querys :
            sort_keyword = ["id","name", "priority"]
            if key_querys["sort"] in sort_keyword :
                product_queryset = product_queryset.order_by(key_querys["sort"])

        if "start" in key_querys :
            product_queryset = product_queryset[int(key_querys["start"]):int(key_querys["start"])+20]

        if "limit" in key_querys :
            product_queryset = product_queryset[:int(key_querys["limit"])]


        product_id_list = [product["id"] for product in product_queryset]
        likes           = Like.objects.filter(product_id__in=product_id_list)
        likes_list      = Counter([like.product_id for like in likes])

        if "detail" in key_querys and key_querys["detail"] == "1" :
            keyword_dicts['mainImg']    = 'product_main_images__main_image_url'
            keyword_dicts['mainImgKey'] = 'product_main_images__product_id'
            product_queryset            = product_queryset.prefetch_related('product_main_images').values(*[keyword_dicts[key] for key in keyword_dicts])
            hash_names_query            = ProductsHashtag.objects.filter(product_id__in=product_id_list).select_related('hashtag').values('hashtag__name','product_id')
            detail_attrs_query          = ProductDetailAttrs.objects.filter(product_id__in=product_id_list)
   
        # 최대 20개로 제한 주기로 함
        for product in product_queryset[:20] :
            curr = {}

            for keys in keyword_dicts :
                curr[keys]   = product[keyword_dicts[keys]]
                curr["like"] = likes_list[product["id"]]

            if "detail" in key_querys and key_querys["detail"] == "1" :
                curr["hashtag"] = [hash['hashtag__name'] for hash in hash_names_query if hash["product_id"] == product["id"]]
                curr["mainImg"] = product["product_main_images__main_image_url"]
                curr["detail"]  = [{
                 "text"      : attrs.text,
                 "priority"  : attrs.priority,
                 "imgDetail" : attrs.image_url
                } for attrs in detail_attrs_query if attrs.product_id == product["id"]]

            result.append(curr)

        print(connection.queries)

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
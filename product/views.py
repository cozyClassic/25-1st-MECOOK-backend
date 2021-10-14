from django.http        import JsonResponse
from product.models     import Products, ProductsHashtag, ProductDetailAttrs
from likes.models       import Like
from django.views       import View
from users.utils        import login_decorator
from collections        import Counter
from django.db.models   import Q

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

keyword_detail_dicts = {
            'mainImg' :'product_main_images__main_image_url',
            'mainImgKey' :'product_main_images__product_id'
        }

@login_decorator
def get_user_id(self,request) :
    return request.user.id

def add_detail_attrs(curr,hash_names_query,product,detail_attrs_query):
    curr["hashtag"] = [hash['hashtag__name'] for hash in hash_names_query if hash["product_id"] == product["id"]]
    curr["mainImg"] = product["product_main_images__main_image_url"]
    curr["detail"]  = [{
        "text"      : attrs.text,
        "priority"  : attrs.priority,
        "imgDetail" : attrs.image_url
    } for attrs in detail_attrs_query if attrs.product_id == product["id"]]
    return curr


def search_keyword_product(request) :
    q_hashtag = Q()
    q_produt  = Q()
    hash_names_query = ProductsHashtag.objects.select_related('hashtag').values('hashtag__name','product_id')

    for keyword in request.GET.getlist("search") :
        q_hashtag.add(Q(hashtag__name__icontains=keyword), q_hashtag.OR)
        q_produt.add(Q(name__icontains=keyword), q_produt.OR)
        
    hashtag_id_list = [mid["product_id"] for mid in hash_names_query.filter(q_hashtag)]   
    q_produt.add(Q(id__in=hashtag_id_list), q_produt.OR)
    return q_produt


class testView(View) :
    def get(self,request) :       
        product_queryset= Products.objects.select_related('category').values(*[keyword_dicts[key] for key in keyword_dicts])
        key_querys      = request.GET
        result          = []

        url_query_parameters = ["product","category","search", "sort","start","limit","detail"]
        for query_param in key_querys :
            if not query_param in url_query_parameters :
                return JsonResponse({ "MESSAGE" : "wrong query keyword" })


        if "product" in key_querys :
            product_queryset = product_queryset.filter(id=key_querys["product"])

        if "category" in key_querys :
            product_queryset = product_queryset.filter(category_id=key_querys["category"])
        
        if "search" in key_querys :
            product_queryset = product_queryset.filter(search_keyword_product(request))
                
        if "sort" in key_querys and  key_querys["sort"] in ["id","name", "priority"] : 
            product_queryset = product_queryset.order_by(key_querys["sort"])

        if "start" in key_querys :
            product_queryset = product_queryset[int(key_querys["start"]):int(key_querys["start"])+20]

        if "limit" in key_querys :
            product_queryset = product_queryset[:int(key_querys["limit"])]

        product_id_list = [product["id"] for product in product_queryset]
        likes           = Like.objects.filter(product_id__in=product_id_list)
        likes_list      = Counter([like.product_id for like in likes])

        if 'Authorization' in request.headers :
            user_id     = get_user_id(self,request)
            like_boolean= [like.product_id for like in likes if like.user_id==user_id]

        if len(product_id_list) == 0 :
            return JsonResponse({"MESSGE" : "EMPTY List"})

        if "detail" in key_querys and key_querys["detail"] == "1" :
            for key in keyword_detail_dicts :
                keyword_dicts[key]  = keyword_detail_dicts[key]
            
            product_queryset    = product_queryset.prefetch_related('product_main_images').values(*[keyword_dicts[key] for key in keyword_dicts])
            hash_names_query    = ProductsHashtag.objects.filter(product_id__in=product_id_list).select_related('hashtag').values('hashtag__name','product_id')
            detail_attrs_query  = ProductDetailAttrs.objects.filter(product_id__in=product_id_list).order_by('priority')
   
        # 최대 20개로 제한 주기로 함
        for product in product_queryset[:20] :
            curr = {}

            for keys in keyword_dicts :
                curr[keys]   = product[keyword_dicts[keys]]
                curr["like"] = likes_list[product["id"]]

            if "detail" in key_querys and key_querys["detail"] == "1" :
                curr = add_detail_attrs(curr,hash_names_query,product,detail_attrs_query)
                
            if 'Authorization' in request.headers :
                curr["this_user_like"] = int(product["id"] in like_boolean)

            result.append(curr)

        return JsonResponse({
            "result" : result
        })

import json

from django.http           import JsonResponse
from django.views          import View
from .models               import Like
from product.models        import Products
from users.utils           import login_decorator

class LikeView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            product_id = data['product']
            product    = Products.objects.get(id=product_id)

            if Like.objects.filter(user=user, product=product).exists():
                Like.objects.filter(user=user, product=product).delete()
                return JsonResponse({"message" : "success"}, status=204)
                
            else:
                Like.objects.create(
                    user    = user,
                    product = product
                )
                return JsonResponse({'message': 'like_success'}, status=201)
        
        except Products.DoesNotExist:
            return JsonResponse({'message': 'item_does_not_exist'}, status=404)

        except KeyError:
            return JsonResponse({'message': 'key_error'}, status=400)

    @login_decorator
    def get(self, request):
        user                = request.user
        user_liked_products = list(Like.objects.filter(user=user).values())

        return JsonResponse({'user': user_liked_products}, status=201)

class AllLikeView(View):
    def get(self, request):
        ret          = []
        product_list = Products.objects.all()

        for product in product_list:
            ret.append({
                'product_id': product.id,
                'count': Like.objects.filter(product=product.id).count()
            })

        return JsonResponse({'like_by_product': ret}, status=201)
        
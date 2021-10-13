import json

from django.http           import JsonResponse
from django.views          import View

from .models               import Carts
from product.models        import Products
from users.utils           import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            Carts.objects.create(
                user     = user,
                product  = Products.objects.get(id=data['product']),
                quantity = data['quantity']
            )
            return JsonResponse({'message': 'added_to_cart'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'key_error'}, status=401)

        except Products.DoesNotExist:
            return JsonResponse({'message': 'item_does_not_exit'}, status=404)

    @login_decorator
    def get(self, request):
        try:
            user = request.user
            cart = Carts.objects.filter(user=user)
            ret  = [{
                    'product_name': item.product.name,
                    'price': item.product.origin_price_KRW,
                    'image': item.product.thumbnail_over_url,
                    'category': item.product.category.name,
                    'quantity': item.quantity,
                    'user': item.user.name,
                    'id': item.id
                }for item in cart]

            return JsonResponse({'cart_info': ret}, status=200)

        except KeyError:
            return JsonResponse({'message': 'key_error'}, status=401)
    
    @login_decorator
    def delete(self, request, cart_id):
        try:
            cart = Carts.objects.get(id=cart_id)
            cart.delete()
            return JsonResponse({'message': 'deleted'}, status=204)

        except Carts.DoesNotExist:
            return JsonResponse({'message': 'nothing_to_delete'}, status=404)

        except KeyError:
            return JsonResponse({'message': 'key_error'}, status=401)
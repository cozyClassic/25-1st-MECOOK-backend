import json

from django.http           import JsonResponse
from django.views          import View
from .models               import Carts
from product.models        import Products
from users.utils           import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = request.user

        Carts.objects.create(
            user = user,
            product = Products.objects.get(id=data['product']),
            quantity = data['quantity']
        )
        return JsonResponse({'message': 'added_to_cart'}, status=201)

    @login_decorator
    def get(self, request):
        user = request.user
        user_cart = Carts.objects.filter(user=user)
        ret = []

        for item in user_cart:
            ret.append({
                'product_name': item.product.name,
                'price': item.product.origin_price_KRW,
                'image': item.product.thumbnail_over_url,
                'category': item.product.category.name,
                'quantity': item.quantity,
                'user': item.user.name,
                'id': item.id
            })

        return JsonResponse({'cart_info': ret}, status=200)
    
    @login_decorator
    def delete(self, request, cart_id):
        authorized_user = request.user
        cart = Carts.objects.get(id=cart_id)
        user = cart.users
        if authorized_user == user:
            cart.delete()
            return JsonResponse({'message': 'deleted'}, status=204)
        else:
            return JsonResponse({'message': 'not_allowed'}, status=400)
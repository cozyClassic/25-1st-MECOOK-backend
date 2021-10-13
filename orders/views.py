import json

from django.http           import JsonResponse
from django.views          import View

from .models               import *
from product.models        import Products
from carts.models          import Carts
from users.utils           import login_decorator

class OrderView(View):
    @login_decorator
    def post(self, request):
        user = request.user
        items = Carts.objects.filter(user=user)

        for item in items:
            int(item.product.origin_price_KRW)
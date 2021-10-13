import json

from django.http           import JsonResponse
from django.views          import View

from .models               import *
from carts.models          import Carts
from users.models          import User
from users.utils           import login_decorator

class OrderView(View):
    @login_decorator
    def post(self, request):
        user = request.user
        Orders.objects.create(
            user = user,
            order = OrderStatus.objects.get(id=1) #OrderStatus id=1일땐 주문완료
        )
        return JsonResponse({'message': 'success'}, status=201)

    @login_decorator
    def get(self, request):
        user = request.user
        items = Carts.objects.filter(user=user)

        total = 0
        for item in items:
            a = int(item.product.origin_price_KRW)
            b = item.quantity
            total += a * b
        print(total)

        user.points -= total
        user.save()

        return JsonResponse({'message': 'point_off'}, status=201)
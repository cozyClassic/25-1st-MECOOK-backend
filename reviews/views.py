import json

from django.http           import JsonResponse
from django.views          import View

from .models               import Reviews
from product.models        import Products
from users.utils           import login_decorator

class ReviewView(View):
    @login_decorator
    def post(self, request):
        try:    
            data        = json.loads(request.body)
            user        = request.user
            product     = Products.objects.get(id=data['product'])

            Reviews.objects.create(
                    user    = user,
                    product = product,
                    review  = data['review'],
            )
            return JsonResponse({'return': 'posted'}, status=201)

        except Products.DoesNotExist:
            return JsonResponse({'message': 'item_does_not_exist'}, status=404)

        except KeyError:
            return JsonResponse({'message': 'key_error'}, status=400)

    def get(self, request, product_id):
        try:
            sort   = request.GET.get('sort', '-created_at')
            offset = int(request.GET.get('offset', 0)) 
            limit  = int(request.GET.get('limit', 5))

            review_by_product = Reviews.objects.filter(product_id=product_id).order_by(sort)[offset:offset+limit]

            ret = [{'review_id': review.id,
                    'review'   : review.review,
                    'product'  : review.product.name,
                    'user'     : review.user.account} for review in review_by_product]

            return JsonResponse({'review_by_product': ret}, status=201)

        except Reviews.DoesNotExist:
            return JsonResponse({'message': 'review_does_not_exits'}, status=404)

        except KeyError:
            return JsonResponse({'message': 'key_error'}, status=400)

    @login_decorator
    def delete(self, request, review_id):
        try:
            review = Reviews.objects.get(id=review_id)
            review.delete()
            return JsonResponse({'message': 'deleted'}, status=204)
        
        except Reviews.DoesNotExist:
            return JsonResponse({'message': 'message_does_not_exist'}, status=404)

        except KeyError:
            return JsonResponse({'message': 'key_error'}, status=400)

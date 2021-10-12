import json

from django.http           import JsonResponse
from django.views          import View
from django.db             import transaction
from .models               import Reviews
from product.models        import Products
from users.utils           import login_decorator

class ReviewView(View):
    @transaction.atomic
    @login_decorator
    def post(self, request):
        try:    
            data        = json.loads(request.body)
            user        = request.user
            product = Products.objects.get(id=data['product'])

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

class GetReviewView(View):

    def get(self, request, product_id):
            review_by_product = Reviews.objects.filter(product_id=product_id)
            ret = []

            for review in review_by_product:
                ret.append({
                    'review_id': review.id,
                    'review'   : review.review,
                    'product'  : review.product.name,
                    'user'     : review.user.account
                })

            return JsonResponse({'review_by_product': ret}, status=201)

class EditReviewView(View):
    @login_decorator
    def delete(self, request, review_id):
        authorized_user = request.user
        review = Reviews.objects.get(id=review_id)
        user = review.user
        if authorized_user == user:
            review.delete()
            return JsonResponse({'message': 'deleted'}, status=204)
        else:
            return JsonResponse({'message': 'not_allowed'}, status=400)
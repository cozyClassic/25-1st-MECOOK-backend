from django.db.models import Model, CharField, ForeignKey, IntegerField, TextField, DateField, IntegerField, CASCADE,BooleanField

# Create your models here.

class Categories(Model) :
    name = CharField(max_length=40)

    class Meta :
        db_table = "categories"


class Products(Model) :
    name                = CharField(max_length=40)
    categoy             = ForeignKey('Categories', on_delete=CASCADE)
    display_0or1        = BooleanField(default=0)
    origin_price_KRW    = IntegerField(default=0)
    discounted_price_KRW= IntegerField(default=0)
    event_price_KRW     = IntegerField(default=0)
    servings_g_people   = CharField(max_length=40)
    detail_top_text     = CharField(max_length=40)
    cook_time           = CharField(max_length=40)
    thumbnail_over_url  = TextField(null=True)
    thumbnail_out_url   = TextField(null=True)
    detail_HTML         = TextField(null=True)
    created_at          = DateField(auto_now_add=True)
    updated_at          = DateField(auto_now=True)
    seller_id           = IntegerField(null=True)

    class Meta :
        db_table= "products"


class Hashtags(Model) :
    name        = CharField(max_length=40)

    class Meta :
        db_table= "hashtags"


class ProductAndHashtag(Model) :
    product  = ForeignKey('Products', on_delete=CASCADE)
    hashtag  = ForeignKey('Hashtags', on_delete=CASCADE)

    class Meta :
        db_table= "product_and_hashtag"


class PriorityOfProducts(Model) :
    priority    = IntegerField(default=0)
    product     = ForeignKey('Products', on_delete=CASCADE)

    class Meta :
        db_table= "priority_of_products"


class product_like_nums(Model) :
    like_num    = IntegerField(default=0)
    product     = ForeignKey('Products', on_delete=CASCADE)

    class Meta :
        db_table= "product_like_nums"
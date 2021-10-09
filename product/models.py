from django.db.models import Model, CharField, ForeignKey, IntegerField, TextField, DateField, IntegerField, CASCADE,BooleanField, DecimalField

# Create your models here.

class Menus(Model) :
    name = CharField(max_length=40)

    class Meta : 
        db_table = "menus"

class Categories(Model) :
    name = CharField(max_length=40)
    menu = ForeignKey('Menus', on_delete=CASCADE)

    class Meta :
        db_table = "categories"


class Products(Model) :
    name                = CharField(max_length=40)
    category            = ForeignKey('Categories', on_delete=CASCADE)
    is_visible          = BooleanField(default=0)
    origin_price_KRW    = DecimalField(default=0, decimal_places=3, max_digits=10)
    discounted_price_KRW= DecimalField(default=0, decimal_places=3, max_digits=10)
    event_price_KRW     = DecimalField(default=0, decimal_places=3, max_digits=10)
    servings_g_people   = CharField(max_length=40)
    cook_time           = CharField(max_length=40)
    detail_top_text     = CharField(max_length=40)
    thumbnail_over_url  = TextField(null=True)
    thumbnail_out_url   = TextField(null=True)
    detail_HTML         = TextField(null=True)
    priority            = IntegerField(default=0)
    seller_id           = IntegerField(null=True)
    created_at          = DateField(auto_now_add=True)
    updated_at          = DateField(auto_now=True)
    deleted_at          = DateField(null=True, default=None)
    
    class Meta :
        db_table= "products"

class ProductsMainImages(Model) :
    main_image_url  = TextField(null=True)
    product         = ForeignKey('Products', on_delete=CASCADE)
    created_at      = DateField(auto_now_add=True)
    updated_at      = DateField(auto_now=True)

    class Meta :
        db_table = "product_main_images"

class Hashtags(Model) :
    name        = CharField(max_length=40)
    created_at  = DateField(auto_now_add=True)
    updated_at  = DateField(auto_now=True)

    class Meta :
        db_table= "hashtags"


class ProductsHashtag(Model) :
    product     = ForeignKey('Products', on_delete=CASCADE)
    hashtag     = ForeignKey('Hashtags', on_delete=CASCADE)
    created_at  = DateField(auto_now_add=True)
    updated_at  = DateField(auto_now=True)

    class Meta :
        db_table= "products_hashtag"

class ProductDetailAttrs(Model) :
    text        = CharField(max_length=100, null=True)
    image_url   = TextField(null=True)
    product     = ForeignKey('Products', on_delete=CASCADE, related_name='product_detail_attrs')
    priority    = IntegerField(default=0)    
    created_at  = DateField(auto_now_add=True)
    updated_at  = DateField(auto_now=True)

    class Meta :
        db_table= "product_detail_attrs"
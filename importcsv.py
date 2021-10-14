import os
import django
import csv


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mecook.settings")
django.setup()

from product.models import ProductDetailAttrs
CSV_PATH_PRODUCTS = 'csv/product_detail_attrs.csv'

with open(CSV_PATH_PRODUCTS) as in_file :
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader :
        ProductDetailAttrs.objects.create(
            text = row[1],
            image_url = row[2],
            priority = row[3],
            product_id=row[4]
            )
"""
from likes.models import Like

CSV_PATH_PRODUCTS = 'csv/likes.csv'

with open(CSV_PATH_PRODUCTS) as in_file :
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader :
        Like.objects.create(
            product_id = row[0],
            user_id = row[1]
            )






CSV_PATH_PRODUCTS = 'csv/menus.csv'

with open(CSV_PATH_PRODUCTS) as in_file :
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader :
        Menus.objects.create(
            name = row[1])

CSV_PATH_PRODUCTS = 'csv/category.csv'

with open(CSV_PATH_PRODUCTS) as in_file :
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader :
        Categories.objects.create(
            name = row[1],
            menu_id=row[2])

CSV_PATH_PRODUCTS = 'csv/product.csv'

with open(CSV_PATH_PRODUCTS) as in_file :
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader :
        Products.objects.create(
            name                = row[1],
            category_id         = row[2],
            is_visible          = row[3],
            origin_price_KRW    = row[4],
            discounted_price_KRW= row[5],
            event_price_KRW     = row[6],
            servings_g_people   = row[7],
            cook_time           = row[8],
            detail_top_text     = row[9],
            thumbnail_over_url  = row[10],
            thumbnail_out_url   = row[11],
            detail_HTML         = row[12],
            priority            = row[13],
            seller_id           = row[14],
            )

CSV_PATH_PRODUCTS = 'csv/product_main_image.csv'

with open(CSV_PATH_PRODUCTS) as in_file :
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader :
        ProductsMainImages.objects.create(
            main_image_url  = row[1],
            product_id      = row[2]
            )

CSV_PATH_PRODUCTS = 'csv/hashtag.csv'

with open(CSV_PATH_PRODUCTS) as in_file :
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader :
        Hashtags.objects.create(
            name = row[1])

CSV_PATH_PRODUCTS = 'csv/product_and_hashtag.csv'

with open(CSV_PATH_PRODUCTS) as in_file :
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader :
        ProductsHashtag.objects.create(
            product_id = row[1],
            hashtag_id = row[2]
            )
"""
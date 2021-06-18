from django.contrib import admin
from .models import (Contact, Product, Category, Brand, Review, VideoReview, ProductImage,
                     CarouselImage, Trending, TrendingOutfit, UserProfile, ProductWithQuantity, MyBag, MyOrder,
                     ReviewCount, ProductDetail, YouWillGet, ProductInfo,
                    ProductSize, ProductColor, VideoReviewCount)
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'is_completed')
    list_filter = ('created_at', 'is_completed')
    search_fields = ['name', 'email', 'phone']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductDetailInline(admin.TabularInline):
    model = ProductDetail
    extra = 3


class YouWillGetInline(admin.TabularInline):
    model = YouWillGet
    extra = 3


class ProductInfoInline(admin.TabularInline):
    model = ProductInfo
    extra = 3


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 3


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'category', 'brand', 'created_at')

    fieldsets = (
        ('Product Details', {
            'fields': ('name', 'price', 'video_details', 'category', 'brand',
                       'is_available', 'has_trial', 'trending_outfit')
        }),
    )

    list_filter = ('created_at', )
    search_fields = ['code', 'name', 'brand']
    inlines = [ProductSizeInline, ProductColorInline, ProductImageInline, ProductDetailInline,
               YouWillGetInline, ProductInfoInline]


admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Trending)
admin.site.register(TrendingOutfit)
admin.site.register(Brand)
admin.site.register(Review)
admin.site.register(ReviewCount)
admin.site.register(VideoReview)
admin.site.register(VideoReviewCount)
admin.site.register(CarouselImage)
# admin.site.register(YouWillGet)    --> we can also access here, but use in inline with product
# admin.site.register(MyBag)


@admin.register(ProductWithQuantity)
class ProductWithQuantityAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'size', 'total_cost')
    fields = ('product', 'quantity', 'size', 'total_cost')
    readonly_fields = ('total_cost', )
    list_filter = ('created_at', )


class ProductWithQuantityInline(admin.TabularInline):
    model = ProductWithQuantity
    extra = 1


@admin.register(MyBag)
class MyBagAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_total', 'user', 'is_send_to_my_order', 'created_at')
    fields = ('sub_total', 'user', 'is_send_to_my_order')
    readonly_fields = ('sub_total',)
    list_filter = ('created_at',)
    inlines = [ProductWithQuantityInline]


# def linkify(field_name):
#     """
#     Converts a foreign key value into clickable links.
#     It will work with list_display list. eg. [linkify(field_name="my_bag")]
#
#     If field_name is 'parent', link text will be str(obj.parent)
#     Link will be admin url for the admin url for obj.parent.id:change
#     """
#     def _linkify(obj):
#         linked_obj = getattr(obj, field_name)
#         if linked_obj is None:
#             return '-'
#         app_label = linked_obj._meta.app_label
#         model_name = linked_obj._meta.model_name
#         view_name = f'admin:{app_label}_{model_name}_change'
#         link_url = reverse(view_name, args=[linked_obj.pk])
#         return format_html('<a href="{}">{}</a>', link_url, linked_obj)
#
#     _linkify.short_description = field_name  # Sets column name
#     return _linkify


@admin.register(MyOrder)
class MyOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'receiver_name', 'receiver_phone',
                    'receiver_division', 'created_at', 'is_confirmed', 'is_canceled', 'is_completed')
    fieldsets = (
        ('Receiver Details', {
            'fields': ('receiver_name', 'receiver_phone', 'receiver_other_phone', 'receiver_division', 'receiver_city',
                       'receiver_area', 'receiver_address')
        }),
        ('Product Details', {
            'fields': ('my_bag', 'user', 'total_product_cost', 'total_payable_with_delivery', 'payment', 'is_confirmed', 'is_canceled'),
            'readonly_fields': ('total_product_cost', 'total_payable_with_delivery')
        }),
        ('Conditions', {
            'fields': ('is_processing', 'is_placed', 'is_on_road', 'is_completed')
        }),
    )
    list_filter = ('created_at', 'is_confirmed', 'is_canceled', 'is_processing', 'is_placed', 'is_on_road',
                   'is_completed', 'receiver_division',
                   'receiver_city', 'receiver_area')
    search_fields = ['order_code', 'user', 'receiver_name', 'receiver_phone']


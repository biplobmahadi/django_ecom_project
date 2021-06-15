from django.contrib import admin
from .models import (Contact, Product, Category, Brand, Review, VideoReview, ProductImage,
                     CarouselImage, Trending, TrendingOutfit, UserProfile, ProductWithQuantity, MyBag, MyOrder,
                     ReviewCount, ProductDetail, YouWillGet, ProductInfo,
                    ProductSize, ProductColor, VideoReviewCount)


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


@admin.register(MyOrder)
class MyOrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'user', 'receiver_name', 'receiver_phone',
                    'receiver_division', 'created_at', 'is_confirm', 'is_payment_confirm', 'is_completed')
    fieldsets = (
        ('Receiver Details', {
            'fields': ('receiver_name', 'receiver_phone', 'receiver_other_phone', 'receiver_division', 'receiver_city',
                       'receiver_area', 'receiver_address')
        }),
        ('Product Details', {
            'fields': ('my_bag', 'user', 'total', 'total_payable', 'payment', 'is_confirm', 'is_payment_confirm')
        }),
        ('Conditions', {
            'fields': ('is_processing', 'is_placed', 'is_on_road', 'is_completed')
        }),
    )
    list_filter = ('created_at', 'is_confirm', 'is_payment_confirm', 'is_processing', 'is_placed', 'is_on_road',
                   'is_completed', 'receiver_division',
                   'receiver_city', 'receiver_area')
    search_fields = ['order_code', 'user', 'receiver_name', 'receiver_phone']


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
admin.site.register(ProductWithQuantity)
admin.site.register(MyBag)

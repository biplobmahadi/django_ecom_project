from django.contrib import admin
from .models import (Contact, Product, Category, SubCategory, Brand, Review, Rating, VideoReview, ProductImage,
                     BackgroudImage, Trending, UserProfile, ProductWithQuantity, MyBag, MyOrder, ReviewCount,
                     VideoReviewCount)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'is_completed')
    list_filter = ('created_at', 'is_completed')
    search_fields = ['name', 'email', 'phone']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'slug', 'price', 'sub_category', 'brand', 'created_at')

    fieldsets = (
        ('Product Details', {
            'fields': ('name', 'price', 'details', 'video_details', 'sub_category', 'brand', 'in_stock', 'trending')
        }),
    )

    list_filter = ('created_at', )
    search_fields = ['code', 'name', 'brand']
    inlines = [ProductImageInline]


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
            'fields': ('my_bag', 'user', 'sub_total', 'total', 'payment', 'is_confirm', 'is_payment_confirm')
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
admin.site.register(SubCategory)
admin.site.register(Trending)
admin.site.register(Brand)
admin.site.register(Review)
admin.site.register(ReviewCount)
# admin.site.register(Rating)
admin.site.register(VideoReview)
admin.site.register(VideoReviewCount)
admin.site.register(BackgroudImage)
admin.site.register(ProductWithQuantity)
admin.site.register(MyBag)

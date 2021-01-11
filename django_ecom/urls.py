from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from all import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # only registered user email can get the email, others can't get the email... it's awesome!!!
    path('password-reset/confirm/<uidb64>/<token>/', TemplateView.as_view(), name='password_reset_confirm'),

    path('admin/', admin.site.urls),

    path('contacts/', views.ContactCreate.as_view()),
    path('product-update-only-quantity/<int:pk>/', views.ProductAvailableRetrieveUpdate.as_view()),
    path('product-images/', views.ProductImageList.as_view()),
    path('product-details/', views.ProductDetailList.as_view()),
    path('you-will-get/', views.YouWillGetList.as_view()),
    path('product-info/', views.ProductInfoList.as_view()),
    path('products/<slug:slug>/', views.ProductRetrieve.as_view()),
    path('category/<slug:slug>/', views.CategoryRetrieve.as_view()),
    path('brands/', views.BrandList.as_view()),
    path('brands/<slug:slug>/', views.BrandRetrieve.as_view()),
    # this is for to access reviewed product from user pages
    path('reviews-read/', views.ReviewRead.as_view()),
    path('reviews-create/', views.ReviewCreate.as_view()),
    path('reviews/<int:pk>/', views.ReviewRetrieveUpdateDestroy.as_view()),
    path('reviews-count-for-agree-update/<int:pk>/', views.ReviewCountForAgreeUpdate.as_view()),
    path('reviews-count-for-disagree-update/<int:pk>/', views.ReviewCountForDisagreeUpdate.as_view()),
    # this is for to access reviewed product from user pages
    path('video-reviews-read/', views.VideoReviewRead.as_view()),
    path('video-reviews-create/', views.VideoReviewCreate.as_view()),
    path('video-reviews/<int:pk>/', views.VideoReviewRetrieveUpdateDestroy.as_view()),
    path('video-reviews-count-for-agree-update/<int:pk>/', views.VideoReviewCountForAgreeUpdate.as_view()),
    path('video-reviews-count-for-disagree-update/<int:pk>/', views.VideoReviewCountForDisagreeUpdate.as_view()),
    path('background-images/', views.BackgroudImageList.as_view()),
    path('trending/<slug:slug>/', views.TrendingRetrieve.as_view()),
    path('trending-outfit/<slug:slug>/', views.TrendingOutfitRetrieve.as_view()),
    path('product-with-quantity/', views.ProductWithQuantityListCreate.as_view()),
    path('product-with-quantity/<int:pk>/', views.ProductWithQuantityRetrieveUpdateDestroy.as_view()),
    path('my-bag/', views.MyBagListCreate.as_view()),
    path('my-bag/<int:pk>/', views.MyBagRetrieveUpdate.as_view()),
    path('my-order/', views.MyOrderListCreate.as_view()),
    path('my-order/<slug:order_code>/', views.MyOrderRetrieveUpdate.as_view()),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('rest-auth/', include('rest_auth.urls')),

    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('rest-auth/social-signup/', TemplateView.as_view(), name='socialaccount_signup'),
    path('rest-auth/varification-email-sent/', TemplateView.as_view(), name='account_email_verification_sent'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""django_ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework import routers
from all import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

# router.register(r'contacts', views.ContactViewSet)
# router.register(r'product-images', views.ProductImageViewSet)
# router.register(r'products', views.ProductViewSet)
# router.register(r'categories', views.CategoryViewSet)
# router.register(r'sub-categories', views.SubCategoryViewSet)
# router.register(r'brands', views.BrandViewSet)
# router.register(r'reviews', views.ReviewViewSet)
# router.register(r'ratings', views.RatingViewSet)
# router.register(r'video-reviews', views.VideoReviewViewSet)
# router.register(r'background-images', views.BackgroudImageViewSet)
# router.register(r'trending', views.TrendingViewSet)
# router.register(r'product-with-quantity', views.ProductWithQuantityViewSet)
# router.register(r'my-bag', views.MyBagViewSet)
# router.register(r'my-order', views.MyOrderViewSet)

urlpatterns = [
path('password-reset/confirm/<uidb64>/<token>/',
        TemplateView.as_view(),
        name='password_reset_confirm'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('contacts/', views.ContactCreate.as_view()),
    path('product-images/', views.ProductImageList.as_view()),
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductRetrieve.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>/', views.CategoryRetrieve.as_view()),
    path('sub-categories/', views.SubCategoryList.as_view()),
    path('sub-categories/<int:pk>/', views.SubCategoryRetrieve.as_view()),
    path('brands/', views.BrandList.as_view()),
    path('brands/<int:pk>/', views.BrandRetrieve.as_view()),
    path('reviews-list/', views.ReviewList.as_view()),
    path('reviews-read/', views.ReviewRead.as_view()),
    path('reviews-create/', views.ReviewCreate.as_view()),
    path('reviews/<int:pk>/', views.ReviewRetrieveUpdateDestroy.as_view()),
    path('reviews-count-update/<int:pk>/', views.ReviewCountUpdate.as_view()),
    # path('ratings-list/', views.RatingList.as_view()),
    # path('ratings-create/', views.RatingCreate.as_view()),
    # path('ratings/<int:pk>/', views.RatingRetrieveUpdateDestroy.as_view()),
    path('video-reviews-list/', views.VideoReviewList.as_view()),
    path('video-reviews-read/', views.VideoReviewRead.as_view()),
    path('video-reviews-create/', views.VideoReviewCreate.as_view()),
    path('video-reviews/<int:pk>/', views.VideoReviewRetrieveUpdateDestroy.as_view()),
    path('video-reviews-count-update/<int:pk>/', views.VideoReviewCountUpdate.as_view()),
    path('background-images/', views.BackgroudImageList.as_view()),
    path('trending/', views.TrendingList.as_view()),
    path('trending/<int:pk>/', views.TrendingRetrieve.as_view()),
    path('product-with-quantity/', views.ProductWithQuantityListCreate.as_view()),
    path('product-with-quantity/<int:pk>/', views.ProductWithQuantityRetrieveUpdateDestroy.as_view()),
    path('my-bag/', views.MyBagListCreate.as_view()),
    path('my-bag/<int:pk>/', views.MyBagRetrieveUpdate.as_view()),
    path('my-order/', views.MyOrderListCreate.as_view()),
    path('my-order/<int:pk>/', views.MyOrderRetrieveUpdate.as_view()),

    # only registered user email can get the email, others can't get the email... it's awesome!!!
  #  url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
  #      TemplateView.as_view(),
  #      name='password_reset_confirm'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('rest-auth/', include('rest_auth.urls')),

    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

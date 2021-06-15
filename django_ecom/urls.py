from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from all import views
from django.conf import settings
from django.conf.urls.static import static

# docs generation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

admin.site.site_header = 'Ignore Administration'    # default: "Django Administration"
admin.site.index_title = 'Features Area'    # default: "Site administration"
admin.site.site_title = 'Ignore Site Admin'    # default: "Django site admin"

urlpatterns = [
    # only registered user email can get the email, others can't get the email... it's awesome!!!
    path('password-reset/confirm/<uidb64>/<token>/', TemplateView.as_view(), name='password_reset_confirm'),

    path('admin/', admin.site.urls),

    path('contact/', views.ContactCreate.as_view()),
    path('product/<slug:slug>/', views.ProductRetrieve.as_view()),
    path('category/<slug:slug>/', views.CategoryRetrieve.as_view()),
    path('brands/', views.BrandList.as_view()),
    path('brand/<slug:slug>/', views.BrandRetrieve.as_view()),
    # this is for to access reviewed product from user pages
    path('reviews/', views.ReviewRead.as_view()),
    path('review-create/', views.ReviewCreate.as_view()),
    path('review/<int:pk>/', views.ReviewUpdateDestroy.as_view()),
    path('review-count-update/<int:pk>/', views.ReviewCountUpdate.as_view()),
    # this is for to access reviewed product from user pages
    path('video-reviews/', views.VideoReviewRead.as_view()),
    path('video-review-create/', views.VideoReviewCreate.as_view()),
    path('video-review/<int:pk>/', views.VideoReviewUpdateDestroy.as_view()),
    path('video-review-count-update/<int:pk>/', views.VideoReviewCountUpdate.as_view()),
    path('carousel-images/', views.CarouselImageList.as_view()),
    path('trending/<slug:slug>/', views.TrendingRetrieve.as_view()),
    path('trending-outfit/<slug:slug>/', views.TrendingOutfitRetrieve.as_view()),
    path('product-with-quantity/', views.ProductWithQuantityCreate.as_view()),
    path('product-with-quantity/<int:pk>/', views.ProductWithQuantityUpdateDestroy.as_view()),
    path('my-bags/', views.MyBagListCreate.as_view()),
    path('my-bag/<int:pk>/', views.MyBagUpdate.as_view()),
    path('my-orders/', views.MyOrderListCreate.as_view()),
    path('my-canceled-orders/', views.MyCanceledOrderList.as_view()),
    path('my-order/<slug:order_code>/', views.MyOrderRetrieveUpdate.as_view()),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('rest-auth/', include('rest_auth.urls')),

    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('rest-auth/social-signup/', TemplateView.as_view(), name='socialaccount_signup'),
    path('rest-auth/varification-email-sent/', TemplateView.as_view(), name='account_email_verification_sent'),

    # doc path
    # path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

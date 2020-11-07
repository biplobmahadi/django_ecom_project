from .models import (Contact, Product, Category, Brand, Review, Rating, VideoReview, ProductImage, BackgroudImage,
                     Trending, SubCategory, ProductWithQuantity, MyBag, MyOrder, ReviewCount, VideoReviewCount)
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, filters
from .serializers import (ContactSerializer, ProductSerializer, CategorySerializer, BrandSerializer, ReviewSerializer,
                          VideoReviewSerializer, ProductImageSerializer, BackgroudImageSerializer,
                          TrendingSerializer, SubCategorySerializer, ProductWithQuantitySerializer, MyBagSerializer,
                          MyOrderSerializer, ProductWithQuantityReadSerializer, MyBagReadSerializer,
                          MyOrderReadSerializer, ReviewCountSerializer, VideoReviewCountSerializer, ReviewReadSerializer, VideoReviewReadSerializer)

from rest_framework.permissions import IsAuthenticated
from all.permissions import IsUserOrReadOnly

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class ContactCreate(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ProductImageList(generics.ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ProductRetrieve(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['category_name']


class CategoryRetrieve(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryList(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class SubCategoryRetrieve(generics.RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class BrandList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['brand_name']


class BrandRetrieve(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ReviewCountUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReviewCount.objects.all()
    serializer_class = ReviewCountSerializer


class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewRead(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewReadSerializer

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)


class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)


#
# class RatingList(generics.ListAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer
#
#
# class RatingCreate(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class RatingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated, IsUserOrReadOnly]
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer


class VideoReviewCountUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VideoReviewCount.objects.all()
    serializer_class = VideoReviewCountSerializer


class VideoReviewList(generics.ListAPIView):
    queryset = VideoReview.objects.all()
    serializer_class = VideoReviewSerializer


class VideoReviewRead(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoReviewReadSerializer

    def get_queryset(self):
        user = self.request.user
        return VideoReview.objects.filter(user=user)


class VideoReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VideoReview.objects.all()
    serializer_class = VideoReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VideoReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]
    serializer_class = VideoReviewSerializer

    def get_queryset(self):
        user = self.request.user
        return VideoReview.objects.filter(user=user)


class BackgroudImageList(generics.ListAPIView):
    queryset = BackgroudImage.objects.all()
    serializer_class = BackgroudImageSerializer


class TrendingList(generics.ListAPIView):
    queryset = Trending.objects.all()
    serializer_class = TrendingSerializer


class TrendingRetrieve(generics.RetrieveAPIView):
    queryset = Trending.objects.all()
    serializer_class = TrendingSerializer


class ProductWithQuantityListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return ProductWithQuantity.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ProductWithQuantityReadSerializer
        return ProductWithQuantitySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class ProductWithQuantityRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return ProductWithQuantity.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ProductWithQuantityReadSerializer
        return ProductWithQuantitySerializer


class MyBagListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return MyBag.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MyBagReadSerializer
        return MyBagSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyBagRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return MyBag.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MyBagReadSerializer
        return MyBagSerializer


class MyOrderListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return MyOrder.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MyOrderReadSerializer
        return MyOrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyOrderRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return MyOrder.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MyOrderReadSerializer
        return MyOrderSerializer

from .models import (Contact, Product, Category, Brand, Review, Rating, VideoReview, ProductImage, BackgroudImage,
                     Trending, TrendingOutfit, ProductWithQuantity, MyBag, MyOrder, ReviewCount, VideoReviewCount,
                     ReviewCountForAgree, ReviewCountForDisagree, ProductDetail, YouWillGet, ProductInfo,
                     ProductAvailable, VideoReviewCountForAgree, VideoReviewCountForDisagree)
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, filters
from .serializers import (ContactSerializer, ProductSerializer, CategorySerializer, BrandSerializer, ReviewSerializer,
                          VideoReviewSerializer, ProductImageSerializer, BackgroudImageSerializer,
                          TrendingSerializer, TrendingOutfitSerializer, ProductWithQuantitySerializer, MyBagSerializer,
                          MyOrderSerializer, ProductWithQuantityReadSerializer, MyBagReadSerializer,
                          MyOrderReadSerializer,
                          ReviewReadSerializer, VideoReviewReadSerializer, ReviewCountForAgreeSerializer,
                          ReviewCountForDisagreeSerializer, ProductDetailSerializer, YouWillGetSerializer,
                          ProductInfoSerializer, ProductAvailableSerializer, VideoReviewCountForAgreeSerializer,
                          VideoReviewCountForDisagreeSerializer)

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


class ProductAvailableUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProductAvailable.objects.all()
    serializer_class = ProductAvailableSerializer


class ProductImageList(generics.ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductDetailList(generics.ListAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer


class YouWillGetList(generics.ListAPIView):
    queryset = YouWillGet.objects.all()
    serializer_class = YouWillGetSerializer


class ProductInfoList(generics.ListAPIView):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer


# its not need maybe
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ProductRetrieve(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


# class CategoryList(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['category_name']
#
#
# class CategoryRetrieve(generics.RetrieveAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     lookup_field = 'slug'


# class SubCategoryList(generics.ListAPIView):
#     queryset = SubCategory.objects.all()
#     serializer_class = SubCategorySerializer


class CategoryRetrieve(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class BrandList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['brand_name']


class BrandRetrieve(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'


# class ReviewCountUpdate(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = ReviewCount.objects.all()
#     serializer_class = ReviewCountSerializer

class ReviewCountForAgreeUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReviewCountForAgree.objects.all()
    serializer_class = ReviewCountForAgreeSerializer

class ReviewCountForDisagreeUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReviewCountForDisagree.objects.all()
    serializer_class = ReviewCountForDisagreeSerializer

# this is not need i think
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


# class VideoReviewCountUpdate(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = VideoReviewCount.objects.all()
#     serializer_class = VideoReviewCountSerializer


class VideoReviewCountForAgreeUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VideoReviewCountForAgree.objects.all()
    serializer_class = VideoReviewCountForAgreeSerializer


class VideoReviewCountForDisagreeUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VideoReviewCountForDisagree.objects.all()
    serializer_class = VideoReviewCountForDisagreeSerializer


# this is not need i think
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

#
# class TrendingList(generics.ListAPIView):
#     queryset = Trending.objects.all()
#     serializer_class = TrendingSerializer
#

class TrendingRetrieve(generics.RetrieveAPIView):
    queryset = Trending.objects.all()
    serializer_class = TrendingSerializer
    lookup_field = 'slug'


class TrendingOutfitRetrieve(generics.RetrieveAPIView):
    queryset = TrendingOutfit.objects.all()
    serializer_class = TrendingOutfitSerializer
    lookup_field = 'slug'


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

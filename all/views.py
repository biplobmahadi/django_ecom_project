from .models import (Contact, Product, Category, Brand, Review, VideoReview, ProductImage, BackgroudImage,
                     Trending, TrendingOutfit, ProductWithQuantity, MyBag, MyOrder,
                     ReviewCountForAgree, ReviewCountForDisagree, ProductDetail, YouWillGet, ProductInfo,
                     ProductAvailable, VideoReviewCountForAgree, VideoReviewCountForDisagree)

from rest_framework import generics, filters
# filters will use when implement search engine
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


class ProductAvailableRetrieveUpdate(generics.RetrieveUpdateAPIView):
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


class ProductRetrieve(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class CategoryRetrieve(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class BrandList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['brand_name']
    # if i implement search then it will use


class BrandRetrieve(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'


class ReviewCountForAgreeUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReviewCountForAgree.objects.all()
    serializer_class = ReviewCountForAgreeSerializer


class ReviewCountForDisagreeUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReviewCountForDisagree.objects.all()
    serializer_class = ReviewCountForDisagreeSerializer


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
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)


class VideoReviewCountForAgreeUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VideoReviewCountForAgree.objects.all()
    serializer_class = VideoReviewCountForAgreeSerializer


class VideoReviewCountForDisagreeUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VideoReviewCountForDisagree.objects.all()
    serializer_class = VideoReviewCountForDisagreeSerializer


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
    permission_classes = [IsAuthenticated]
    serializer_class = VideoReviewSerializer

    def get_queryset(self):
        user = self.request.user
        return VideoReview.objects.filter(user=user)


class BackgroudImageList(generics.ListAPIView):
    queryset = BackgroudImage.objects.all()
    serializer_class = BackgroudImageSerializer


class TrendingRetrieve(generics.RetrieveAPIView):
    queryset = Trending.objects.all()
    serializer_class = TrendingSerializer
    lookup_field = 'slug'


class TrendingOutfitRetrieve(generics.RetrieveAPIView):
    queryset = TrendingOutfit.objects.all()
    serializer_class = TrendingOutfitSerializer
    lookup_field = 'slug'


class ProductWithQuantityListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ProductWithQuantity.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ProductWithQuantityReadSerializer
        return ProductWithQuantitySerializer


class MyBagListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MyBag.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MyBagReadSerializer
        return MyBagSerializer


class MyOrderListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_code'

    def get_queryset(self):
        user = self.request.user
        return MyOrder.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MyOrderReadSerializer
        return MyOrderSerializer

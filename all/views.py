from .models import (Contact, Product, Category, Brand, Review, VideoReview, ProductImage, CarouselImage,
                     Trending, TrendingOutfit, ProductWithQuantity, MyBag, MyOrder,
                     ReviewCount, ProductDetail, YouWillGet, ProductInfo, VideoReviewCount)
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView,
                                     ListCreateAPIView, RetrieveUpdateAPIView)
# filters will use when implement search engine
from .serializers import (ContactSerializer, ProductSerializer, CategorySerializer, BrandSerializer, ReviewSerializer,
                          VideoReviewSerializer, ProductImageSerializer, CarouselImageSerializer,
                          TrendingSerializer, TrendingOutfitSerializer, ProductWithQuantitySerializer, MyBagSerializer,
                          MyOrderSerializer, ProductWithQuantityReadSerializer, MyBagReadSerializer,
                          MyOrderReadSerializer, ReviewReadSerializer, VideoReviewReadSerializer, ReviewCountSerializer,
                          ProductDetailSerializer, YouWillGetSerializer, ProductInfoSerializer,
                          VideoReviewCountSerializer)

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


class ContactCreate(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ProductRetrieve(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class CategoryRetrieve(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class BrandList(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['brand_name']
    # if i implement search then it will use


class BrandRetrieve(RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'


class ReviewCountUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReviewCount.objects.all()
    serializer_class = ReviewCountSerializer


class ReviewRead(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewReadSerializer

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)


class ReviewCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewUpdateDestroy(UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)


class VideoReviewCountUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VideoReviewCount.objects.all()
    serializer_class = VideoReviewCountSerializer


class VideoReviewRead(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoReviewReadSerializer

    def get_queryset(self):
        user = self.request.user
        return VideoReview.objects.filter(user=user)


class VideoReviewCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VideoReview.objects.all()
    serializer_class = VideoReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VideoReviewUpdateDestroy(UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoReviewSerializer

    def get_queryset(self):
        user = self.request.user
        return VideoReview.objects.filter(user=user)


class CarouselImageList(ListAPIView):
    queryset = CarouselImage.objects.all()
    serializer_class = CarouselImageSerializer


class TrendingRetrieve(RetrieveAPIView):
    queryset = Trending.objects.all()
    serializer_class = TrendingSerializer
    lookup_field = 'slug'


class TrendingOutfitRetrieve(RetrieveAPIView):
    queryset = TrendingOutfit.objects.all()
    serializer_class = TrendingOutfitSerializer
    lookup_field = 'slug'


class ProductWithQuantityCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProductWithQuantity.objects.all()
    serializer_class = ProductWithQuantitySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductWithQuantityUpdateDestroy(UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProductWithQuantity.objects.all()
    serializer_class = ProductWithQuantitySerializer


class MyBagListCreate(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MyBag.objects.filter(user=user, is_send_to_my_order=False)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MyBagReadSerializer
        return MyBagSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyBagUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MyBag.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MyBagReadSerializer
        return MyBagSerializer


class MyOrderListCreate(ListCreateAPIView):
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


class MyOrderRetrieveUpdate(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MyOrder.objects.all()
    lookup_field = 'order_code'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MyOrderReadSerializer
        return MyOrderSerializer


# just list here, to see details we can use MyOrderRetrieveUpdate and can re confirm by this
# but we differentiate it to make a filter easily, to get fast load advantage
class MyCanceledOrderList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyOrderReadSerializer

    def get_queryset(self):
        user = self.request.user
        return MyOrder.objects.filter(user=user, is_canceled=True)

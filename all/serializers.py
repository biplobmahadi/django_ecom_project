from rest_framework import serializers
from .models import (Contact, Product, Category, Brand, Review, VideoReview, ProductImage, CarouselImage,
                     Trending, TrendingOutfit, ProductWithQuantity, MyBag, MyOrder,
                     ReviewCount, ProductDetail, YouWillGet, ProductInfo,
                     ProductSize, ProductColor, VideoReviewCount)
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.models import User
from rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_auth.registration.serializers import RegisterSerializer
# for sending mail
from django.core.mail import send_mail

# division, city, area select choice option set here
# need to update city and area
DIVISION_SELECT = (
    ('Dhaka', 'Dhaka'),
    ('Chittagong', 'Chittagong'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Sylhet', 'Sylhet'),
    ('Barisal', 'Barisal'),
    ('Rangpur', 'Rangpur'),
    ('Mymensingh', 'Mymensingh'),
)
CITY_SELECT = (
    ('Dhaka', 'Dhaka'),
    ('Chittagong', 'Chittagong'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Sylhet', 'Sylhet'),
    ('Barisal', 'Barisal'),
    ('Rangpur', 'Rangpur'),
    ('Mymensingh', 'Mymensingh'),
)
AREA_SELECT = (
    ('Dhaka', 'Dhaka'),
    ('Chittagong', 'Chittagong'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Sylhet', 'Sylhet'),
    ('Barisal', 'Barisal'),
    ('Rangpur', 'Rangpur'),
    ('Mymensingh', 'Mymensingh'),
)


class MyRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])
########################## custom mail sending for confirm registration, but smtp already send varification like mailgun
#         name = user.first_name
#         email = user.email
#         subject = 'Confirm your account'
#         message = f'''Hi {name},
# Your email is: {email}'''
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [email]
#         send_mail(subject, message, email_from, recipient_list, fail_silently=False)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        ###### FILTER USER MODEL ######
        if not User.objects.filter(email=value).exists():
            # if user not register then email will not send
            raise serializers.ValidationError(_('This e-mail address is not registered'))
        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),

            ###### USE TEXT FILE ######
            'email_template_name': 'password_reset_email.txt',
            'request': request,
        }
        self.reset_form.save(**opts)


class UserSerializer(UserDetailsSerializer):
    phone = PhoneNumberField(source="userprofile.phone", allow_blank=True)
    division = serializers.ChoiceField(source="userprofile.division", choices=DIVISION_SELECT, allow_blank=True)
    city = serializers.ChoiceField(source="userprofile.city", choices=CITY_SELECT, allow_blank=True)
    area = serializers.ChoiceField(source="userprofile.area", choices=AREA_SELECT, allow_blank=True)
    address = serializers.CharField(source="userprofile.address", style={'base_template': 'textarea.html'}, allow_blank=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('phone', 'division', 'city', 'area', 'address')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        phone = profile_data.get('phone')
        division = profile_data.get('division')
        city = profile_data.get('city')
        area = profile_data.get('area')
        address = profile_data.get('address')
        instance = super(UserSerializer, self).update(instance, validated_data)
        # get and update user profile
        profile = instance.userprofile
        if profile_data:
            profile.phone = phone
            profile.division = division
            profile.city = city
            profile.area = area
            profile.address = address
            profile.save()
        return instance


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'message']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = '__all__'


class YouWillGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouWillGet
        fields = '__all__'


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = '__all__'


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = '__all__'


class ReviewCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewCount
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    review_count = ReviewCountSerializer(read_only=True, many=True)

    class Meta:
        model = Review
        fields = ['id', 'review_detail', 'rating_star', 'product', 'user', 'review_count', 'created_at']


class VideoReviewCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoReviewCount
        fields = '__all__'


class VideoReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    video_review_count = VideoReviewCountSerializer(read_only=True, many=True)

    class Meta:
        model = VideoReview
        fields = ['id', 'link', 'product', 'user', 'video_review_count', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True)
    video_review = VideoReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'slug', 'name', 'price', 'brand', 'video_details',
                  'product_image', 'is_available', 'has_trial', 'review', 'video_review',
                  'product_detail', 'you_will_get', 'product_info', 'product_color', 'product_size']
        depth = 1


class ReviewReadSerializer(ReviewSerializer):
    product = ProductSerializer(read_only=True)


class VideoReviewReadSerializer(VideoReviewSerializer):
    product = ProductSerializer(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'slug', 'category_name', 'category_img', 'product']


class BrandSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Brand
        fields = ['id', 'slug', 'brand_name', 'brand_img', 'product']


class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = ['id', 'image', 'is_active']


class TrendingOutfitSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = TrendingOutfit
        fields = ['id', 'slug', 'trend_outfit_name', 'trend_outfit_img', 'product']


class TrendingSerializer(serializers.ModelSerializer):
    trending_outfit = TrendingOutfitSerializer(many=True)

    class Meta:
        model = Trending
        fields = ['id', 'slug', 'trend_name', 'trend_img', 'trending_outfit']


class ProductWithQuantitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductWithQuantity
        fields = '__all__'
        read_only_fields = ['user']


class ProductWithQuantityReadSerializer(ProductWithQuantitySerializer):
    product = ProductSerializer(read_only=True)


class MyBagSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = MyBag
        fields = '__all__'


class MyBagReadSerializer(MyBagSerializer):
    product_with_quantity = ProductWithQuantityReadSerializer(read_only=True, many=True)


class MyOrderSerializer(serializers.ModelSerializer):
   # user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = MyOrder
        fields = '__all__'
        read_only_fields = ['user']
# because here i only get user pk. not username... so i will edit this __all__ with actual name and also user


class MyOrderReadSerializer(MyOrderSerializer):
    my_bag = MyBagReadSerializer(read_only=True)

from rest_framework import serializers
from .models import (Contact, Product, Category, Brand, Review, Rating, VideoReview, ProductImage, BackgroudImage,
                     Trending, TrendingOutfit, SubCategory, ProductWithQuantity, MyBag, MyOrder, ReviewCount, VideoReviewCount,
                     ReviewCountForAgree, ReviewCountForDisagree,)
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.models import User
from rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_auth.registration.serializers import RegisterSerializer


class MyRegisterSerializer(RegisterSerializer):

  first_name = serializers.CharField(required=True)
  last_name = serializers.CharField(required=True)

  def custom_signup(self, request, user):
    user.first_name = self.validated_data.get('first_name', '')
    user.last_name = self.validated_data.get('last_name', '')
    user.save(update_fields=['first_name', 'last_name'])


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        ###### FILTER YOUR USER MODEL ######
        if not User.objects.filter(email=value).exists():

            raise serializers.ValidationError(_('This e-mail address is not registered'))
        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),

            ###### USE YOUR TEXT FILE ######
            'email_template_name': 'password_reset_email.txt',

            'request': request,
        }
        self.reset_form.save(**opts)


class UserSerializer(UserDetailsSerializer):
    # full_name = serializers.CharField(source="userprofile.full_name", allow_blank=True)
    phone = PhoneNumberField(source="userprofile.phone", allow_blank=True)
    DIVISION_SELECT = (
        ('Dhaka', 'Dhaka'),
        ('Chottogram', 'Chottogram'),
        ('Rajshahi', 'Rajshahi'),
        ('Sylhet', 'Sylhet'),
    )
    division = serializers.ChoiceField(source="userprofile.division", choices=DIVISION_SELECT, allow_blank=True)
    CITY_SELECT = (
        ('Dhaka', 'Dhaka'),
        ('Chottogram', 'Chottogram'),
        ('Rajshahi', 'Rajshahi'),
        ('Sylhet', 'Sylhet'),
    )
    city = serializers.ChoiceField(source="userprofile.city", choices=CITY_SELECT, allow_blank=True)
    AREA_SELECT = (
        ('Dhaka', 'Dhaka'),
        ('Chottogram', 'Chottogram'),
        ('Rajshahi', 'Rajshahi'),
        ('Sylhet', 'Sylhet'),
    )
    area = serializers.ChoiceField(source="userprofile.area", choices=AREA_SELECT, allow_blank=True)
    address = serializers.CharField(source="userprofile.address", style={'base_template': 'textarea.html'}, allow_blank=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('phone', 'division', 'city', 'area', 'address')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        # full_name = profile_data.get('full_name')
        phone = profile_data.get('phone')
        division = profile_data.get('division')
        city = profile_data.get('city')
        area = profile_data.get('area')
        address = profile_data.get('address')
        instance = super(UserSerializer, self).update(instance, validated_data)
        # get and update user profile
        profile = instance.userprofile
        if profile_data:
            # profile.full_name = full_name
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





class ReviewCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewCount
        fields = '__all__'


class ReviewCountForAgreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewCountForAgree
        fields = '__all__'


class ReviewCountForDisagreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewCountForDisagree
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.userprofile')
    user = UserSerializer(read_only=True)
    # this is for instance
    # reviewcount = ReviewCountSerializer(read_only=True)
    reviewcountforagree = ReviewCountForAgreeSerializer(read_only=True)
    reviewcountfordisagree = ReviewCountForDisagreeSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'review_detail', 'rating_star', 'product', 'user', 'reviewcountforagree', 'reviewcountfordisagree']


class VideoReviewCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoReviewCount
        fields = '__all__'


class VideoReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    videoreviewcount = VideoReviewCountSerializer(read_only=True)

    class Meta:
        model = VideoReview
        fields = ['id', 'link', 'product', 'user', 'videoreviewcount']


class ProductSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True)
    video_review = VideoReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'slug', 'code', 'name', 'price', 'sub_category', 'brand', 'details', 'video_details', 'trending_outfit',
                  'product_image', 'in_stock', 'review', 'video_review']
# why don't I get review here
        depth = 2
# I change this position in 16 nov


class ReviewReadSerializer(ReviewSerializer):
    product = ProductSerializer(read_only=True)


#
# class RatingSerializer(serializers.ModelSerializer):
#     # user = serializers.ReadOnlyField(source='user.userprofile.full_name')
#
#     class Meta:
#         model = Rating
#         fields = '__all__'
#         read_only_fields = ['user']


class VideoReviewReadSerializer(VideoReviewSerializer):
    product = ProductSerializer(read_only=True)


class SubCategorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'slug', 'category', 'sub_category_name', 'sub_category_img', 'product']


class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'slug', 'category_name', 'sub_category']


class BrandSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Brand
        fields = ['id', 'slug', 'brand_name', 'brand_img', 'product']


class BackgroudImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroudImage
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
    product = ProductWithQuantityReadSerializer(read_only=True, many=True)


class MyOrderSerializer(serializers.ModelSerializer):
   # user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = MyOrder
        fields = '__all__'
        read_only_fields = ['user']
# because here i only get user pk. not username... so i will edit this __all__ with actual name and also user


class MyOrderReadSerializer(MyOrderSerializer):
    my_bag = MyBagReadSerializer(read_only=True)

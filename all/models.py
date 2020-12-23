from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

DIVISION_SELECT = (
        ('Dhaka', 'Dhaka'),
        ('Chottogram', 'Chottogram'),
        ('Rajshahi', 'Rajshahi'),
        ('Sylhet', 'Sylhet'),
    )
CITY_SELECT = (
    ('Dhaka', 'Dhaka'),
    ('Chottogram', 'Chottogram'),
    ('Rajshahi', 'Rajshahi'),
    ('Sylhet', 'Sylhet'),
)
AREA_SELECT = (
    ('Dhaka', 'Dhaka'),
    ('Chottogram', 'Chottogram'),
    ('Rajshahi', 'Rajshahi'),
    ('Sylhet', 'Sylhet'),
    ('mamaaaa', 'mamaaaa'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # custom fields for user
    # full_name = models.CharField(max_length=100, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    division = models.CharField(max_length=100, choices=DIVISION_SELECT, blank=True, null=True)
    city = models.CharField(max_length=100, choices=CITY_SELECT, blank=True, null=True)
    area = models.CharField(max_length=100, choices=AREA_SELECT, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Contact(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = PhoneNumberField()
    message = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    slug = models.SlugField(max_length=50, help_text='set a slug for url', unique=True, editable=False)
    category_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.category_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.category_name}'


class SubCategory(models.Model):
    slug = models.SlugField(max_length=50, help_text='set a slug for url', unique=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='sub_category')
    sub_category_name = models.CharField(max_length=50, unique=True)
    sub_category_img = models.ImageField(upload_to='sub_category_img')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.sub_category_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Category: {self.category} -> Sub-Category: {self.sub_category_name}'


class Brand(models.Model):
    slug = models.SlugField(max_length=50, help_text='set a slug for url', unique=True, editable=False)
    brand_name = models.CharField(max_length=50, unique=True)
    brand_img = models.ImageField(upload_to='brand_img')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.brand_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.brand_name


class Trending(models.Model):
    slug = models.SlugField(max_length=50, help_text='set a slug for url', unique=True, editable=False)
    trend_name = models.CharField(max_length=50)
    trend_img = models.ImageField(upload_to='trend_img')
    # trend_outfit_name = models.CharField(max_length=50, unique=True)
    # trend_outfit_img = models.ImageField(upload_to='trend_outfit_img')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.trend_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Season: {self.trend_name}'


class TrendingOutfit(models.Model):
    slug = models.SlugField(max_length=50, help_text='set a slug for url', unique=True, editable=False)
    # trend_name = models.CharField(max_length=50)
    # trend_img = models.ImageField(upload_to='trend_img')
    trending = models.ForeignKey(Trending, on_delete=models.SET_NULL, null=True, related_name='trending_outfit')
    trend_outfit_name = models.CharField(max_length=50, unique=True)
    trend_outfit_img = models.ImageField(upload_to='trend_outfit_img')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.trend_outfit_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Season: {self.trending.trend_name} -> Outfit: {self.trend_outfit_name}'


class Product(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=150, help_text='set a slug for url', unique=True, editable=False)
    # slug max_lenght more than name because of there price will include
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='product')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='product')
    trending_outfit = models.ForeignKey(TrendingOutfit, on_delete=models.SET_NULL, null=True, blank=True, related_name='product')
    in_stock = models.BooleanField(default=True)
    details = models.TextField(max_length=500)
    # details field will redesign after everything in product
    video_details = models.URLField(help_text='provide a youtube link')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.name + f'-{self.price}' + '-tk'
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Name: {self.name} -> Price: {self.price}'


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')

    def __str__(self):
        return f'{self.image}'


class Review(models.Model):
    review_detail = models.TextField()
    rating_star = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review PK: -> {self.id}'


class ReviewCount(models.Model):
    pass
#
# class ReviewCount(models.Model):
#     review = models.OneToOneField(Review, on_delete=models.CASCADE)
#     agreed = models.PositiveIntegerField(default=0)
#     disagreed = models.PositiveIntegerField(default=0)
#     user = models.ManyToManyField(User, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'Review PK: -> {self.review.id}'
#
#
# @receiver(post_save, sender=Review)
# def create_review_count(sender, instance, created, **kwargs):
#     if created:
#         ReviewCount.objects.create(review=instance)
#
#
# @receiver(post_save, sender=Review)
# def save_review_count(sender, instance, **kwargs):
#     instance.reviewcount.save()


class ReviewCountForAgree(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    agreed = models.PositiveIntegerField(default=0)
    user = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review PK: -> {self.review.id}'


@receiver(post_save, sender=Review)
def create_review_count_for_agree(sender, instance, created, **kwargs):
    if created:
        ReviewCountForAgree.objects.create(review=instance)


@receiver(post_save, sender=Review)
def save_review_count_for_agree(sender, instance, **kwargs):
    instance.reviewcountforagree.save()


class ReviewCountForDisagree(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    disagreed = models.PositiveIntegerField(default=0)
    user = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review PK: -> {self.review.id}'


@receiver(post_save, sender=Review)
def create_review_count_for_disagree(sender, instance, created, **kwargs):
    if created:
        ReviewCountForDisagree.objects.create(review=instance)


@receiver(post_save, sender=Review)
def save_review_count_for_disagree(sender, instance, **kwargs):
    instance.reviewcountfordisagree.save()


class Rating(models.Model):
    pass


class VideoReview(models.Model):
    link = models.URLField(help_text='provide a youtube link')
    # rating_star = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='video_review')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Video Review PK: -> {self.id}'


class VideoReviewCount(models.Model):
    video_review = models.OneToOneField(VideoReview, on_delete=models.CASCADE)
    agreed = models.PositiveIntegerField(default=0)
    disagreed = models.PositiveIntegerField(default=0)
    user = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Video Review PK: -> {self.video_review.id}'

# have a problem here
# solved

@receiver(post_save, sender=VideoReview)
def create_video_review_count(sender, instance, created, **kwargs):
    if created:
        VideoReviewCount.objects.create(video_review=instance)


@receiver(post_save, sender=VideoReview)
def save_video_review_count(sender, instance, **kwargs):
    instance.videoreviewcount.save()


class ProductWithQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product_with_quantity')
    quantity = models.PositiveIntegerField(default=1)
    cost = models.PositiveIntegerField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Product: {self.product} -> Quantity: {self.quantity}'


class MyBag(models.Model):
    product = models.ManyToManyField(ProductWithQuantity, related_name='my_bag', blank=True)
    sub_total = models.PositiveIntegerField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_send_to_my_order = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Total product in bag: {self.product.all().count()} -> User: {self.user.username}'


class MyOrder(models.Model):
    # slug = models.SlugField(max_length=50, help_text='set a slug for url', unique=True, editable=False)
    order_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    my_bag = models.OneToOneField(MyBag, on_delete=models.DO_NOTHING, related_name='my_order')
    sub_total = models.PositiveIntegerField(blank=True, null=True)
    total = models.PositiveIntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    receiver_name = models.CharField(max_length=30, blank=True)
    receiver_phone = PhoneNumberField(blank=True)
    receiver_other_phone = PhoneNumberField(blank=True)
    receiver_division = models.CharField(max_length=100, choices=DIVISION_SELECT, blank=True)
    receiver_city = models.CharField(max_length=100, choices=CITY_SELECT, blank=True)
    receiver_area = models.CharField(max_length=100, choices=AREA_SELECT, blank=True)
    receiver_address = models.TextField(max_length=200, blank=True)
    is_confirm = models.BooleanField(default=False)
    is_payment_confirm = models.BooleanField(default=False)
    payment = models.CharField(blank=True, null=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processing = models.BooleanField(default=False)
    is_placed = models.BooleanField(default=False)
    is_on_road = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'Code: {self.order_code} -> User: {self.user.username}'


class BackgroudImage(models.Model):
    image = models.ImageField(upload_to='background_image')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.image}'

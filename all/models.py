from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

# size set for select choice option
SIZE_SELECT = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
    ('XXXL', 'XXXL'),
)

# payment set for select choice option
PAYMENT_SELECT = (
    ('Cash On Delivery', 'Cash On Delivery'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # custom fields for user where one user have only one profile
    phone = PhoneNumberField(blank=True, null=True)
    division = models.CharField(max_length=100, choices=DIVISION_SELECT, blank=True, null=True)
    city = models.CharField(max_length=100, choices=CITY_SELECT, blank=True, null=True)
    area = models.CharField(max_length=100, choices=AREA_SELECT, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username


# create the instance for user and userprofile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = PhoneNumberField()
    message = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    category_name = models.CharField(max_length=50, unique=True, help_text="eg. (Men's Pant, Women's Shirt, IPhone, Football)")
    category_img = models.ImageField(upload_to='category_img')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.category_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Category: {self.category_name}'


class Brand(models.Model):
    slug = models.SlugField(max_length=50, unique=True, editable=False)
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
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    trend_name = models.CharField(max_length=50, unique=True)
    trend_img = models.ImageField(upload_to='trend_img')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.trend_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Season: {self.trend_name}'


class TrendingOutfit(models.Model):
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    trending = models.ForeignKey(Trending, on_delete=models.CASCADE, related_name='trending_outfit')
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
    slug = models.SlugField(max_length=150, unique=True, editable=False)
    # slug max_length more than name because of there price will include
    name = models.CharField(max_length=100, unique=True)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='product')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='product')
    trending_outfit = models.ForeignKey(TrendingOutfit, on_delete=models.SET_NULL, null=True, blank=True, related_name='product')

    has_size = models.BooleanField(default=False)
    has_trial = models.BooleanField(default=False)

    video_details = models.URLField(help_text='provide a youtube link')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.name + f'-{self.price}' + '-tk'
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Name: {self.name} -> Price: {self.price}'


class ProductAvailable(models.Model):
    available_quantity = models.PositiveIntegerField(default=5)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    # this relationship is perfect
    # one product has only one ProductAvailable

    def __str__(self):
        return f'Available -> {self.available_quantity}'

# here, relationship for product for multiple option is perfect
# when we set available, one product has only one. then the rltn is onetoone
# but we can set multiple gift, detail, image, info for one single product thats why they are foreignkey rltn


class ProductDetail(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_detail')
    # these relationship is perfect also

    def __str__(self):
        return f'{self.title} -> {self.value}'


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')

    def __str__(self):
        return f'{self.image}'


class YouWillGet(models.Model):
    gift = models.CharField(max_length=100, help_text='eg. (2 Lottery, One IPhone 12 Max Pro)')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='you_will_get')

    def __str__(self):
        return f'{self.gift}'


class ProductInfo(models.Model):
    info = models.CharField(max_length=100, help_text='eg. (6 Months Warranty, 3 Month Guaranty)')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_info')

    def __str__(self):
        return f'{self.info}'


class Review(models.Model):
    review_detail = models.TextField()
    rating_star = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    # here use auto_now=True, because when user update then this date will auto update

    def __str__(self):
        return f'Review PK: -> {self.id}'


class ReviewCountForAgree(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    agreed = models.PositiveIntegerField(default=0)
    user = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review PK: {self.review.id} and agreed {self.agreed}'


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
        return f'Review PK: -> {self.review.id} and disagreed {self.disagreed}'


@receiver(post_save, sender=Review)
def create_review_count_for_disagree(sender, instance, created, **kwargs):
    if created:
        ReviewCountForDisagree.objects.create(review=instance)


@receiver(post_save, sender=Review)
def save_review_count_for_disagree(sender, instance, **kwargs):
    instance.reviewcountfordisagree.save()


class VideoReview(models.Model):
    link = models.URLField(help_text='provide a youtube link')
    # this will no rating, only review
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='video_review')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True) 
    # here use auto_now=True, because when user update then this date will auto update

    def __str__(self):
        return f'Video Review PK: -> {self.id}'


class VideoReviewCountForAgree(models.Model):
    video_review = models.OneToOneField(VideoReview, on_delete=models.CASCADE)
    agreed = models.PositiveIntegerField(default=0)
    user = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Video Review PK: -> {self.video_review.id} and agreed {self.agreed}'


@receiver(post_save, sender=VideoReview)
def create_video_review_count_for_agree(sender, instance, created, **kwargs):
    if created:
        VideoReviewCountForAgree.objects.create(video_review=instance)


@receiver(post_save, sender=VideoReview)
def save_video_review_count_for_agree(sender, instance, **kwargs):
    instance.videoreviewcountforagree.save()


class VideoReviewCountForDisagree(models.Model):
    video_review = models.OneToOneField(VideoReview, on_delete=models.CASCADE)
    disagreed = models.PositiveIntegerField(default=0)
    user = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review PK: -> {self.video_review.id} and disagreed {self.disagreed}'


@receiver(post_save, sender=VideoReview)
def create_video_review_count_for_disagree(sender, instance, created, **kwargs):
    if created:
        VideoReviewCountForDisagree.objects.create(video_review=instance)


@receiver(post_save, sender=VideoReview)
def save_video_review_count_for_disagree(sender, instance, **kwargs):
    instance.videoreviewcountfordisagree.save()


class ProductWithQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product_with_quantity')
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, choices=SIZE_SELECT, blank=True)
    cost = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_as_trial = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Product: {self.product} -> Quantity: {self.quantity}'


class MyBag(models.Model):
    product_with_quantity = models.ManyToManyField(ProductWithQuantity, related_name='my_bag', blank=True)
    sub_total = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_send_to_my_order = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Total product in bag: {self.product_with_quantity.all().count()} -> User: {self.user.username}'


class MyOrder(models.Model):
    order_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    my_bag = models.OneToOneField(MyBag, on_delete=models.DO_NOTHING, related_name='my_order')
    total = models.PositiveIntegerField()
    total_payable = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    receiver_name = models.CharField(max_length=30, blank=True)
    receiver_phone = PhoneNumberField(blank=True)
    receiver_other_phone = PhoneNumberField(blank=True)
    receiver_division = models.CharField(max_length=100, choices=DIVISION_SELECT, blank=True)
    receiver_city = models.CharField(max_length=100, choices=CITY_SELECT, blank=True)
    receiver_area = models.CharField(max_length=100, choices=AREA_SELECT, blank=True)
    receiver_address = models.TextField(max_length=200, blank=True)

    is_confirm = models.BooleanField(default=False)
    is_payment_confirm = models.BooleanField(default=False)

    payment = models.CharField(max_length=100, choices=PAYMENT_SELECT, blank=True)
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

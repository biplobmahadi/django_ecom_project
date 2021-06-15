# Generated by Django 3.1.5 on 2021-06-15 18:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('brand_name', models.CharField(max_length=50, unique=True)),
                ('brand_img', models.ImageField(upload_to='brand_img')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='background_image')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('category_name', models.CharField(help_text="eg. (Men's Pant, Women's Shirt, IPhone, Football)", max_length=50, unique=True)),
                ('category_img', models.ImageField(upload_to='category_img')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('message', models.TextField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MyBag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_total', models.PositiveIntegerField()),
                ('is_send_to_my_order', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(editable=False, max_length=150, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('price', models.PositiveIntegerField()),
                ('has_trial', models.BooleanField(default=False)),
                ('is_available', models.BooleanField(default=False)),
                ('video_details', models.URLField(help_text='provide a youtube link')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='all.brand')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='all.category')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_detail', models.TextField()),
                ('rating_star', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='all.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('trend_name', models.CharField(max_length=50, unique=True)),
                ('trend_img', models.ImageField(upload_to='trend_img')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(help_text='provide a youtube link')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_review', to='all.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='YouWillGet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gift', models.CharField(help_text='eg. (2 Lottery, One IPhone 12 Max Pro)', max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='you_will_get', to='all.product')),
            ],
        ),
        migrations.CreateModel(
            name='VideoReviewCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreed', models.BooleanField(default=False)),
                ('disagreed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_review_count', to='all.videoreview')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('division', models.CharField(blank=True, choices=[('Dhaka', 'Dhaka'), ('Chittagong', 'Chittagong'), ('Rajshahi', 'Rajshahi'), ('Khulna', 'Khulna'), ('Sylhet', 'Sylhet'), ('Barisal', 'Barisal'), ('Rangpur', 'Rangpur'), ('Mymensingh', 'Mymensingh')], max_length=100, null=True)),
                ('city', models.CharField(blank=True, choices=[('Dhaka', 'Dhaka'), ('Chittagong', 'Chittagong'), ('Rajshahi', 'Rajshahi'), ('Khulna', 'Khulna'), ('Sylhet', 'Sylhet'), ('Barisal', 'Barisal'), ('Rangpur', 'Rangpur'), ('Mymensingh', 'Mymensingh')], max_length=100, null=True)),
                ('area', models.CharField(blank=True, choices=[('Dhaka', 'Dhaka'), ('Chittagong', 'Chittagong'), ('Rajshahi', 'Rajshahi'), ('Khulna', 'Khulna'), ('Sylhet', 'Sylhet'), ('Barisal', 'Barisal'), ('Rangpur', 'Rangpur'), ('Mymensingh', 'Mymensingh')], max_length=100, null=True)),
                ('address', models.TextField(blank=True, max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrendingOutfit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('trend_outfit_name', models.CharField(max_length=50, unique=True)),
                ('trend_outfit_img', models.ImageField(upload_to='trend_outfit_img')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('trending', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trending_outfit', to='all.trending')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreed', models.BooleanField(default=False)),
                ('disagreed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_count', to='all.review')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductWithQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('size', models.CharField(blank=True, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')], max_length=10)),
                ('color', models.CharField(blank=True, choices=[('Black', 'Black'), ('Green', 'Green'), ('Red', 'Red')], max_length=20)),
                ('cost', models.PositiveIntegerField()),
                ('add_as_trial', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_with_quantity', to='all.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')], max_length=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_size', to='all.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(help_text='eg. (6 Months Warranty, 3 Month Guaranty)', max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_info', to='all.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='all.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_detail', to='all.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('Black', 'Black'), ('Green', 'Green'), ('Red', 'Red')], max_length=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_color', to='all.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='trending_outfit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='all.trendingoutfit'),
        ),
        migrations.CreateModel(
            name='MyOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('total', models.PositiveIntegerField()),
                ('total_payable', models.PositiveIntegerField()),
                ('receiver_name', models.CharField(blank=True, max_length=30)),
                ('receiver_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('receiver_other_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('receiver_division', models.CharField(blank=True, choices=[('Dhaka', 'Dhaka'), ('Chittagong', 'Chittagong'), ('Rajshahi', 'Rajshahi'), ('Khulna', 'Khulna'), ('Sylhet', 'Sylhet'), ('Barisal', 'Barisal'), ('Rangpur', 'Rangpur'), ('Mymensingh', 'Mymensingh')], max_length=100)),
                ('receiver_city', models.CharField(blank=True, choices=[('Dhaka', 'Dhaka'), ('Chittagong', 'Chittagong'), ('Rajshahi', 'Rajshahi'), ('Khulna', 'Khulna'), ('Sylhet', 'Sylhet'), ('Barisal', 'Barisal'), ('Rangpur', 'Rangpur'), ('Mymensingh', 'Mymensingh')], max_length=100)),
                ('receiver_area', models.CharField(blank=True, choices=[('Dhaka', 'Dhaka'), ('Chittagong', 'Chittagong'), ('Rajshahi', 'Rajshahi'), ('Khulna', 'Khulna'), ('Sylhet', 'Sylhet'), ('Barisal', 'Barisal'), ('Rangpur', 'Rangpur'), ('Mymensingh', 'Mymensingh')], max_length=100)),
                ('receiver_address', models.TextField(blank=True, max_length=200)),
                ('is_confirm', models.BooleanField(default=False)),
                ('is_payment_confirm', models.BooleanField(default=False)),
                ('payment', models.CharField(blank=True, choices=[('Cash On Delivery', 'Cash On Delivery')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_processing', models.BooleanField(default=False)),
                ('is_placed', models.BooleanField(default=False)),
                ('is_on_road', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('my_bag', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='my_order', to='all.mybag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mybag',
            name='product_with_quantity',
            field=models.ManyToManyField(blank=True, related_name='my_bag', to='all.ProductWithQuantity'),
        ),
        migrations.AddField(
            model_name='mybag',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

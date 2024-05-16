from django.db import models
from django.utils import timezone
from extentions.utils import jalali_convertor
from django.contrib.auth.models import User

#my managers
class ArticleManager(models.Manager):
    def published (self):
        return self.filter(status = 'p')

class CategoryManager(models.Manager):
    def active (self):
        return self.filter(status = True)

class category(models.Model):
    parent = models.ForeignKey('self', default = None, null = True, blank = True, on_delete = models.SET_NULL, related_name = 'children', verbose_name = "زیردسته")
    title = models.CharField(max_length= 200, verbose_name = "عنوان دسته‌بندی")
    slug = models.SlugField (max_length = 100, unique=True, verbose_name = "آدرس دسته‌بندی")
    status = models.BooleanField(default = True, verbose_name = "آیا نمایش داده شود؟")
    position = models.IntegerField(verbose_name = "پوزیشن")

    class Meta(object):
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی ها"
        ordering = ['parent__id','position']

    def __str__(self):
        return self.title

    objects = CategoryManager()
    
    def get_published_articles(self):
        """Returns all published articles in this category."""
        return self.articles.filter(status='p')

    def get_child_categories(self):
        """Returns all child categories of this category."""
        return self.children.all()

class Article(models.Model):
    STATUS_CHOICES = (
    ('d', 'پیش نویس'),
    ('p', 'منتشر شده'),
    )
    title = models.CharField(max_length= 200, verbose_name = "عنوان مقاله")
    weight = models.CharField(max_length=20, verbose_name= "وزن")
    price = models.IntegerField(verbose_name = "قیمت")
    slug = models.SlugField (max_length = 100, unique=True, verbose_name = "آدرس مقاله")
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ManyToManyField(category, verbose_name = "دسته‌بندی", related_name = "articles")
    description = models.TextField (verbose_name = "محتوا")
    thumbnail = models.ImageField (upload_to="images", verbose_name = " تصویر")
    publish = models.DateTimeField (default = timezone.now, verbose_name = "زمان انتشار")
    created = models.DateTimeField (auto_now_add = True, verbose_name = "زمان ساخت")
    updated = models.DateTimeField (auto_now = True)
    status = models.CharField (max_length = 1, choices = STATUS_CHOICES, verbose_name = "وضعیت")
    class Meta(object):
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"


    def __str__(self):
        return self.title

    def jpublish(self):
        return jalali_convertor(self.publish)
    jpublish.short_description = "زمان انتشار"

    def category_published(self):
        return self.category.filter(status = True)

    objects = ArticleManager()
    
    def is_published(self):
        """Checks if the article is published."""
        return self.status == 'p'

    def get_jalali_publish_date(self):
        """Converts and returns the publish date in Jalali (Persian) calendar."""
        return jalali_convertor(self.publish)

    def get_related_categories(self):
        """Returns all categories associated with this article."""
        return self.category_published()

    def get_thumbnail_url(self):
        """Returns the URL of the article's thumbnail."""
        return self.thumbnail.url

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}'s Address"
    
    def get_full_address(self):
        """Returns the full address string."""
        return f"{self.street}, {self.city}, {self.province}, {self.zip_code}"


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def get_full_name(self):
        """Returns the full name of the user."""
        return f"{self.name} {self.last_name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    @property
    def total_price(self):
        total = sum(item.total_price for item in self.items.all())
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price
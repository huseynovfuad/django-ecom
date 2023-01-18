from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from services.mixin import DateMixin, SlugMixin
from services.uploader import Uploader
from services.generator import Generator
from services.choices import SIZES
from django.contrib.auth import get_user_model
from .validators import name_validator
from PIL import Image

# Create your models here.

User = get_user_model()

class Size(DateMixin):
    name = models.CharField(max_length=200, choices=SIZES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Size"
        verbose_name_plural = "Sizes"



class Category(MPTTModel, DateMixin, SlugMixin):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to=Uploader.upload_images_to_categories, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=10, model_=Category)
        super(Category, self).save(*args, **kwargs)


class Product(DateMixin, SlugMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, validators=[name_validator])
    wishlist = models.ManyToManyField(User, blank=True, related_name="wishlist")
    description = RichTextField()
    price = models.FloatField()
    tax = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    sizes = models.ManyToManyField(Size, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=10, model_=Product)
        super(Product, self).save(*args, **kwargs)

    # def total_price(self):
    #     return self.price + (self.tax or 0) - (self.discount or 0)



class ProductImage(DateMixin, SlugMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Uploader.upload_images_to_products)

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=10, model_=ProductImage)
        if not self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                new_img = (300, 300)
                img.thumbnail(new_img)
                img.save(self.image.path)

        super(ProductImage, self).save(*args, **kwargs)



class Comment(MPTTModel, DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.email} --> {self.product.name}"

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


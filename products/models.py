from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from services.mixin import DateMixin, SlugMixin
from services.uploader import Uploader
from services.generator import Generator
from services.choices import SIZES

# Create your models here.

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
        self.slug = Generator.create_slug_shortcode(size=10, model_=Category)
        super(Category, self).save(*args, **kwargs)


class Product(DateMixin, SlugMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
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
        self.slug = Generator.create_slug_shortcode(size=10, model_=Product)
        super(Product, self).save(*args, **kwargs)

    def total_price(self):
        return self.price + (self.tax or 0) - (self.discount or 0)



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
        self.slug = Generator.create_slug_shortcode(size=10, model_=ProductImage)
        super(ProductImage, self).save(*args, **kwargs)


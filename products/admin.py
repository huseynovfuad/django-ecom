from django.contrib import admin
from .models import (
    Product, ProductImage, Category, Size, Comment
)

# Register your models here.

class MixinAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)


class CategoryAdmin(MixinAdmin):
    class Meta:
        model = Category

    list_display = MixinAdmin.list_display + ("created_at", )


admin.site.register(Category, CategoryAdmin)


class ImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    max_num = 10

class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product

    inlines = [ImageInline]

    list_display = ("category", "name", "slug", "created_at")
    search_fields = ("name", )
    list_filter = ("category", "created_at")


admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)
admin.site.register(Size)
admin.site.register(Comment)
from django.db import models
from django.contrib.auth import get_user_model
from services.mixin import DateMixin, SlugMixin
from services.uploader import Uploader
from services.generator import Generator

# Create your models here.

User = get_user_model()


class Profile(DateMixin, SlugMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateTimeField(blank=True, null=True)
    avatar = models.ImageField(upload_to=Uploader.upload_images_to_profile, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ("-created_at", )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=10, model_=Profile)
        super(Profile, self).save(*args, **kwargs)


class DeletedProfile(models.Model):
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username

from .models import User, Profile, DeletedProfile


from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


@receiver(post_save, sender=User)
def user_save_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_delete, sender=User)
def user_save_signal(sender, instance, **kwargs):
    DeletedProfile.objects.create(
        username=instance.username,
        first_name=instance.first_name,
        last_name=instance.last_name,
    )
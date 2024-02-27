from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import ActivityList

@receiver(post_save, sender=ActivityList)
def update_activity_cache(sender, instance, **kwargs):
    cache.delete('list_of_activity')

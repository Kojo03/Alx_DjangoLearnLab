from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(recipient, actor, verb, target=None):
    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=ContentType.objects.get_for_model(target) if target else None,
        object_id=target.id if target else None,
    )

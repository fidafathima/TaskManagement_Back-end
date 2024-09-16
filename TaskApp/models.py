import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


class UserDetails(AbstractUser):
    is_user=models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    email = models.EmailField()


def __str__(self):
    return self.name
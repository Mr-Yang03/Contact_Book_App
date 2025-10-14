from django.db import models
from django.utils import timezone


class Group(models.Model):
    """
    Model đại diện cho một nhóm liên hệ, ví dụ: Gia đình, Đồng nghiệp.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    """
    Model lưu trữ thông tin chi tiết của một liên hệ.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    address = models.CharField(max_length=255, blank=True)
    birthday = models.DateField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="contacts",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()
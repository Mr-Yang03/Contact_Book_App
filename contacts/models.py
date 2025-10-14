from django.db import models
from django.utils import timezone


class Group(models.Model):
    """
    Model đại diện cho một nhóm liên hệ, ví dụ: Gia đình, Đồng nghiệp.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên Nhóm")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Nhóm"
        verbose_name_plural = "Các Nhóm"


class Contact(models.Model):
    """
    Model lưu trữ thông tin chi tiết của một liên hệ.
    """
    # Thông tin cơ bản
    first_name = models.CharField(max_length=50, verbose_name="Tên")
    last_name = models.CharField(max_length=50, verbose_name="Họ")

    # Thông tin liên lạc
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="Số điện thoại")
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="Email")

    # Thông tin bổ sung
    address = models.CharField(max_length=255, blank=True, verbose_name="Địa chỉ")
    birthday = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")

    # Mối quan hệ Nhiều-Nhiều với Group
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="contacts",
        verbose_name="Thuộc Nhóm"
    )

    # Dấu thời gian
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lúc")

    def get_full_name(self):
        """Trả về tên đầy đủ của liên hệ."""
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "Liên hệ"
        verbose_name_plural = "Các Liên hệ"
        ordering = ['first_name', 'last_name']  # Sắp xếp theo tên
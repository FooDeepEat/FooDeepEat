from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


# 유저 정보 테이블
class Account(AbstractUser):
    birth_date = models.DateField(default=datetime.date.today)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=13)

    def __str__(self):
        return f"{self.email} {self.username} {self.password}"


# 유저 프로필 사진
class ProfileImage(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='profile_images')
    profile_img = models.ImageField(null=True, blank=True, upload_to="profile/")
    img_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.profile_img}"


# 유저 주소 테이블
class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='addresses')
    postal_code = models.IntegerField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} {self.postal_code} {self.city} {self.address}"


# 유저 선택 정보 테이블
class Option(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='option')
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} {self.height} {self.weight} {self.gender}"


# 유저 동의 테이블
class Agree(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='agree')
    must_agree = models.CharField(max_length=10)
    option_agree = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username} {self.must_agree} {self.option_agree}"

from django.db import models
from django.contrib.auth.models import AbstractUser


# 유저 정보 테이블
class Account(AbstractUser):
    # 오늘보다 과거인 날짜만 입력 할 수 있음
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=15)

    def __str__(self):
        return f"이메일:{self.email} 아이디:{self.username} 비밀번호:{self.password}"


# 유저 프로필 사진
class ProfileImage(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='profile')
    profile_img = models.ImageField(upload_to="profile/")
    img_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"유저:{self.user.username} 이미지:{self.profile_img}"


# 유저 주소 테이블
class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='addresses')
    postal_code = models.IntegerField()
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"유저:{self.user.username} 우편번호:{self.postal_code} 도시:{self.city} 상세주소:{self.address}"


# 유저 선택 정보 테이블
class Option(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='option')
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    gender = models.CharField(max_length=1)

    def __str__(self):
        return f"유저:{self.user.username} 키:{self.height} 몸무게:{self.weight}"


# 유저 동의 테이블
class Agree(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='agree')
    must_agree = models.BooleanField()
    option_agree = models.BooleanField()

    def __str__(self):
        return f"유저:{self.user.username} 필수동의:{self.must_agree} 선택동의:{self.option_agree}"

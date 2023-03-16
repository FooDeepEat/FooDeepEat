from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from phone_field import PhoneField
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Invalid phone number."
)


# 유저 정보 테이블
class User(AbstractUser):
    birth_date = models.DateField(db_column="birth_date",
                                  validators=[MinValueValidator(timezone.localdate()),  # 현재 날짜 이전이어야 함
                                              MaxValueValidator(timezone.localdate()),  # 현재 날짜 이후이어야 함
                                              ], default="1900-01-01", null=False)
    email = models.EmailField(db_column="user_email", null=False, unique=True)
    # phone_number = PhoneField(db_column="phone_number", default="010-0000-0000", null=False)
    phone_number = models.CharField(validators=[phone_validator], null=False, unique=True, max_length=15)

    def __str__(self):
        return f"이메일:{self.email} 아이디:{self.username} 비밀번호:{self.password}"


# 유저 프로필 사진
class UserProfileImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    profile_img = models.ImageField(null=True, blank=True, default='', upload_to="profile/")

    def __str__(self):
        return f"유저:{self.user.username} 이미지:{self.profile_img}"


# 유저 주소 테이블
class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    postal_code = models.IntegerField(null=False)
    city = models.CharField(null=False, max_length=100)
    address = models.CharField(null=True, blank=True, max_length=255, default='')

    def __str__(self):
        return f"유저:{self.user.username} 우편번호:{self.postal_code} 도시:{self.city} 상세주소:{self.address}"


# 유저 선택 정보 테이블
class UserOption(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='option')
    height = models.PositiveIntegerField(null=True, blank=True, default='')
    weight = models.PositiveIntegerField(null=True, blank=True, default='')
    gender = models.CharField(null=True, blank=True, default='', max_length=10)

    def __str__(self):
        return f"유저:{self.user.username} 키:{self.height} 몸무게:{self.weight}"


# 유저 동의 테이블
class UserAgree(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agree')
    must_agree = models.BooleanField(default=True)
    option_agree = models.BooleanField(default=False)

    def __str__(self):
        return f"유저:{self.user.username} 필수동의:{self.must_agree} 선택동의:{self.option_agree}"

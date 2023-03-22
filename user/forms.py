from django import forms
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from .models import Account, Address, Option, Agree, ProfileImage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.db import transaction
from django.utils import timezone


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    birth_date = forms.DateField(
        validators=[MinValueValidator(timezone.now().date() - timezone.timedelta(days=365 * 100)),
                    MaxValueValidator(timezone.now().date())], required=True)
    phone_number = forms.CharField(
        validators=[RegexValidator(r'^01\d{1}-\d{3,4}-\d{4}$')],
        required=True, max_length=15)
    postal_code = forms.IntegerField(required=True)
    city = forms.CharField(max_length=30, required=True)
    address = forms.CharField(max_length=100, required=False)
    must_agree = forms.BooleanField()
    option_agree = forms.BooleanField()
    height = forms.IntegerField(min_value=0, max_value=300, required=True)
    weight = forms.IntegerField(min_value=0, max_value=300, required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)
    profile_img = forms.ImageField(
        required=False,
        widget=ClearableFileInput(attrs={'accept': 'image/*'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            raise ValidationError("이메일이 이미 존재합니다.")
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("이메일 형식이 맞지 않습니다.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Account.objects.filter(username=username).exists():
            raise ValidationError("아이디가 이미 존재합니다.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError:
            raise ValidationError("비밀번호 형식이 맞지 않습니다.")
        return password

    def save(self):
        data = self.cleaned_data
        with transaction.atomic():
            user = Account.objects.create_user(username=data['username'], email=data['email'], password=data['password'],
                                               first_name=data['first_name'], last_name=data['last_name'],
                                               birth_date=data['birth_date'], phone_number=data['phone_number'])
            Address.objects.create(postal_code=data['postal_code'], city=data['city'], address=data['address'],
                                   user=user)
            Option.objects.create(height=data['height'], weight=data['weight'], gender=data['gender'], user=user)
            Agree.objects.create(must_agree=data['must_agree'], option_agree=data['option_agree'], user=user)
            if data['profile_img']:
                profile_img = ProfileImage(profile_img=data['profile_img'], user=user)
                profile_img.save()
            else:
                ProfileImage.objects.create(user=user)
            return user

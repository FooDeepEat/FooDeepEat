from django import forms
from django.forms import DateInput
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm
from .models import Account, ProfileImage, Address, Option, Agree
from django.core.validators import MinValueValidator, MaxValueValidator


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        required=True
    )
    birth_date = forms.DateField(
        validators=[
            MinValueValidator(timezone.now().date() - timezone.timedelta(days=365 * 100)),
            MaxValueValidator(timezone.now().date())
        ],
        widget=DateInput(attrs={'type': 'date'}),
        required=True
    )
    phone_number = forms.CharField(
        max_length=13,
        help_text='전화번호를 입력하세요. (ex: 010-1234-5678)',
        validators=[
            RegexValidator(r'^01[0-9]{1}-[0-9]{3,4}-[0-9]{4}$')
        ],
        required=True
    )

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name',
                  'birth_date', 'phone_number', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            raise ValidationError("이메일이 이미 존재합니다.")
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("이메일 형식이 맞지 않습니다.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Account.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("전화번호가 이미 존재합니다.")
        return phone_number


class ProfileImageForm(forms.ModelForm):
    profile_img = forms.ImageField(
        widget=ClearableFileInput(attrs={'accept': 'image/*'}),
        required=False
    )

    class Meta:
        model = ProfileImage
        fields = ('profile_img',)

    def clean_profile_img(self):
        profile_img = self.cleaned_data.get('profile_img')
        if profile_img:
            if profile_img.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError("파일 크기는 5MB 이하여야 합니다.")
            return profile_img
        return None


class AddressForm(forms.ModelForm):
    postal_code = forms.IntegerField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=True
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=True
    )
    address = forms.CharField(
        max_length=100,
        required=False
    )

    class Meta:
        model = Address
        fields = ('postal_code', 'city', 'address')


class OptionForm(forms.ModelForm):
    height = forms.IntegerField(
        min_value=0,
        max_value=300,
        required=False
    )
    weight = forms.IntegerField(
        min_value=0,
        max_value=300,
        required=False
    )
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female')],
        required=True
    )

    class Meta:
        model = Option
        fields = ('height', 'weight', 'gender')


class AgreeForm(forms.ModelForm):
    must_agree = forms.ChoiceField(
        choices=[('agree', '동의합니다.'), ('disagree', '동의하지 않습니다.')],
        widget=forms.RadioSelect,
        required=True,
    )
    option_agree = forms.ChoiceField(
        choices=[('agree', '동의합니다.'), ('disagree', '동의하지 않습니다.')],
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = Agree
        fields = ('must_agree', 'option_agree')

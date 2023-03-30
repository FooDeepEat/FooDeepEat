from django import forms
from django.forms import DateInput, ClearableFileInput
from django.utils import timezone
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import Account, Address, Option, Agree, ProfileImage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'autofocus': True}),
        required=True,
    )
    last_name = forms.CharField(
        max_length=15,
        required=True,
    )
    birth_date = forms.DateField(
        validators=[
            MinValueValidator(timezone.now().date() - timezone.timedelta(days=365 * 100)),
            MaxValueValidator(timezone.now().date())
        ],
        widget=DateInput(attrs={'type': 'date'}),
        required=True,
    )
    phone_number = forms.CharField(
        max_length=13,
        validators=[
            RegexValidator(r'^\d{3}-\d{4}-\d{4}$')
        ],
        required=True
    )
    password1 = forms.CharField(
        validators=[
            # 최소 길이 8 ~ 최대 길이 12
            MinLengthValidator(8),
            MaxLengthValidator(12)
        ],
        widget=forms.PasswordInput(attrs={'placeholder': '최소8자리 이상 ~ 최대 12자리 이하'})
    )

    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'phone_number', 'password1', 'password2', 'email')


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
        choices=[('', '선택'), ('M', 'Male'), ('F', 'Female')],
        required=False
    )

    class Meta:
        model = Option
        fields = ('height', 'weight', 'gender')


class AgreeForm(forms.ModelForm):
    must_agree = forms.ChoiceField(
        choices=[('agree', '동의합니다.'), ('disagree', '동의하지 않습니다.')],
        widget=forms.RadioSelect(),
        required=True,
    )
    option_agree = forms.ChoiceField(
        choices=[('agree', '동의합니다.'), ('disagree', '동의하지 않습니다.')],
        widget=forms.RadioSelect(),
        required=True,
    )

    class Meta:
        model = Agree
        fields = ('must_agree', 'option_agree')


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

from django.urls import reverse_lazy

from . import models
from .forms import SignUpForm, AddressForm, OptionForm, AgreeForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from food_deep_eat import settings
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import string
import re
import random


def generate_code(length):
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def create_forms(request):
    return {
        'signup_form': SignUpForm(request.POST),
        'address_form': AddressForm(request.POST),
        'option_form': OptionForm(request.POST),
        'agree_form': AgreeForm(request.POST)
    }


class CleandForm:
    def __init__(self, request):
        self.request = request

    def email(self):
        email = self.request.POST.get('username')
        try:
            validate_email(email)
        except ValidationError:
            email_error = "이메일 형식이 올바르지 않습니다."
            return email_error
        else:
            email_exists = models.Account.objects.filter(username=email).exists()
            if email_exists:
                email_error = "이미 사용중인 이메일입니다."
                return email_error
        return email

    def phone(self):
        phone_number = self.request.POST.get('phone_number')
        if not re.match(r'^\d{3}-\d{4}-\d{4}$', phone_number):
            phone_error = "전화번호 형식이 올바르지 않습니다. (예시: 010-1234-5678)"
            return phone_error

        phone_exists = models.Account.objects.filter(phone_number=phone_number).exists()
        if phone_exists:
            phone_error = "이미 사용중인 전화번호입니다."
            return phone_error

    def password(self):
        password1 = self.request.POST.get('password1')
        password2 = self.request.POST.get('password2')
        if not re.search(r'(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}', password1):
            pw_error = "비밀번호는 영문, 숫자, 특수문자가 포함된 8자 이상이어야 합니다."
            return pw_error
        if password1 != password2:
            pw_error = "패스워드가 일치하지 않습니다."
            return pw_error


def register(request):
    if request.method == 'POST':
        # 이메일 인증코드 발송 기능
        if 'auth_code' in request.POST:
            username = CleandForm(request).email()
            if '@' not in username:
                return render(request, 'register/register.html',
                              {**create_forms(request), 'email_error': username})
            else:
                subject = '푸디핏 회원가입 인증코드입니다.'
                from_email = settings.EMAIL_HOST_USER
                # 이메일을 받을 수신자의 리스트
                recipient_list = [username]
                auth_code = generate_code(6)
                request.session['auth_code'] = auth_code
                message = '안녕하세요. 푸디핏입니다.'
                html_message = f'<p>건강한 식생활 라이프스타일 서포터 푸디핏입니다.</p>' \
                               f'<p>고객님께서 요청하신 이메일 인증 코드를 발송해 드립니다.</p>' \
                               f'<p>아래 6자리 코드를 복사하셔서 회원가입 시에 사용해 주세요.</p>' \
                               f'<p><strong>인증코드:</strong> {auth_code}</p>'
                send_mail(subject, message, from_email, recipient_list, html_message=html_message)
                email_success = '이메일이 전송되었습니다. 메일함을 확인해주세요'
                return render(request, 'register/register.html',
                              {**create_forms(request), 'email_success': email_success})

        # 이메일 인증코드 확인
        elif 'check_code' in request.POST:
            valid_code = request.POST.get('emailcheck')
            if valid_code == request.session.get('auth_code'):
                valid_success = "인증에 성공하셨습니다."
                return render(request, "register/register.html", {**create_forms(request),
                                                                  "valid_success": valid_success,
                                                                  "valid_code": valid_code})
            else:
                valid_error = "인증에 실패하셨습니다."
            return render(request, "register/register.html", {**create_forms(request), "valid_error": valid_error})

        else:
            phone_error = CleandForm(request).phone()
            pw_error = CleandForm(request).password()
            if phone_error or pw_error:
                return render(request, 'register/register.html', {**create_forms(request),
                                                                  "phone_error": phone_error or None,
                                                                  "pw_error": pw_error or None})
            forms = create_forms(request)
            if all(form.is_valid() for form in forms.values()):
                with transaction.atomic():
                    user = forms['signup_form'].save(commit=False)
                    user.email = user.username
                    user.save()
                    for form_name, form in forms.items():
                        if form_name != 'signup_form':
                            form_object = form.save(commit=False)
                            form_object.user = user
                            form_object.save()
                return render(request, 'register/register_done.html')

            else:
                for form_name, form in forms.items():
                    if not form.is_valid():
                        errors = form.errors
                        print(errors)

    # 새롭게 딕셔너리를 생성하지 않고 있는 그대로 보냄
    return render(request, 'register/register.html', create_forms(request))


@login_required
def register_edit(request):
    user = request.user

    account = models.Account.objects.filter(username=user.username).first()
    address = models.Address.objects.filter(user_id=account.id).first()
    option = models.Option.objects.filter(user_id=account.id).first()
    agree = models.Agree.objects.filter(user_id=account.id).first()

    if request.method == "POST":
        if 'delete_user' in request.POST:
            user.delete()
            return redirect('logout')

        elif 'edit_user' in request.POST:
            with transaction.atomic():
                account.phone_number = request.POST['phone_number']
                account.birth_date = request.POST['birth_date']
                address.postal_code = request.POST['postal_code']
                address.city = request.POST['city']
                address.address = request.POST['address']
                agree.must_agree = request.POST['must_agree']
                option.gender = request.POST['gender']
                option.height = request.POST['height']
                option.weight = request.POST['weight']
                agree.option_agree = request.POST['option_agree']

                account.save()
                address.save()
                agree.save()
                option.save()
            return redirect('calorie:mypage')

    form={
        'signup_form': SignUpForm(instance=account),
        'address_form': AddressForm(instance=address),
        'option_form': OptionForm(instance=option),
        'agree_form': AgreeForm(instance=agree)
    }
    return render(request, "register/register_edit.html", {"form": form, "account": account})


# 아이디 찾기
def find_username(request):
    if request.method == "POST":
        first_name = request.POST['name'][:1]
        last_name = request.POST['name'][1:]
        birth_date = request.POST['birth_date']
        try:
            user = models.Account.objects.get(first_name=first_name, last_name=last_name,
                                              birth_date=birth_date)
            return render(request, 'find_username.html', {"find_username": user.username})
        except models.Account.DoesNotExist:
            error_msg = '등록 된 계정이 없습니다.'
            return render(request, 'find_username.html', {"error_msg": error_msg})

    return render(request, 'find_username.html')


def logout_view(request):
    logout(request)
    return redirect("calorie:home")


class MyLoginView(LoginView):
    template_name = 'login.html'


class PWResetView(PasswordResetView):
    template_name = 'password_reset/pw_reset.html'
    email_template_name = 'password_reset/pw_reset_email.html'
    subject_template_name = 'password_reset/pw_reset_email.txt'

    def form_valid(self, form):
        email = self.request.POST.get('email')
        first_name = self.request.POST.get('name')[:1]
        last_name = self.request.POST.get('name')[1:]
        birth_date = self.request.POST.get("birth_date")
        phone_number = self.request.POST.get("number")

        if not models.Account.objects.filter(email=email,
                                             first_name=first_name,
                                             last_name=last_name,
                                             phone_number=phone_number,
                                             birth_date=birth_date).exists():
            error_msg = "이메일 또는 이름을 다시 확인해주세요."
            return render(self.request, 'password_reset/pw_reset.html', {"error_msg": error_msg})
        else:
            return super().form_valid(form)


class PWResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset/pw_reset_done.html'


class PWResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset/pw_reset_confirm.html'


class PWResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset/pw_reset_complete.html'

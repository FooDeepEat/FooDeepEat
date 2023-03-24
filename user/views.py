from . import models
from .forms import SignUpForm, ProfileImageForm, AddressForm, OptionForm, AgreeForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect
from django.db import transaction


def create_forms(request):
    return {
        'signup_form': SignUpForm(request.POST),
        'profile_form': ProfileImageForm(request.FILES, request.POST)
        if 'auth' not in request.POST
        else ProfileImageForm(request.FILES, request.POST),
        'address_form': AddressForm(request.POST),
        'option_form': OptionForm(request.POST),
        'agree_form': AgreeForm(request.POST)
    }


def register(request):
    if request.method == 'POST':
        if 'auth' in request.POST:  # 중복 체크 버튼을 눌렀을 때
            username = request.POST.get('username', '')
            user_exists = models.Account.objects.filter(username=username).exists()
            user_msg = '이미 사용중인 유저네임입니다.' if user_exists else '사용 가능한 유저네임입니다.'
            # user_msg를 딕셔너리에 추가해서 보내기 위해 **create_forms 새로운 딕셔너리 생성
            return render(request, 'register/register.html', {**create_forms(request), 'user_msg': user_msg})

        else:
            forms = create_forms(request)
            if all(form.is_valid() for form in forms.values()):
                with transaction.atomic():
                    user = forms['signup_form'].save()

                    for form_name, form in forms.items():
                        if form_name != 'signup_form':
                            form_object = form.save(commit=False)
                            form_object.user = user
                            form_object.save()

                return redirect('login')
            else:
                for form_name, form in forms.items():
                    if not form.is_valid():
                        errors = form.errors
                        print(errors)
    # 새롭게 딕셔너리를 생성하지 않고 있는 그대로 보냄
    return render(request, 'register/register.html', create_forms(request))


# 아이디 찾기
def find_id(request):
    if request.method == "POST":
        email = request.POST["email"]
        first_name = request.POST['name'][:1]
        last_name = request.POST['name'][1:]
        birth_date = request.POST['birth_date']
        # print(request.POST)
        try:
            user = models.Account.objects.get(email=email, first_name=first_name, last_name=last_name,
                                              birth_date=birth_date)
            return render(request, 'find_id.html', {"find_id": user.username})
        except models.Account.DoesNotExist:
            error_msg = '등록 된 계정은 없습니다.'
            return render(request, 'find_id.html', {"error_msg": error_msg})

    return render(request, 'find_id.html')


def logout_view(request):
    logout(request)
    return redirect("calorie:home")


class LoginView(LoginView):
    template_name = 'login.html'


class PWResetView(PasswordResetView):
    template_name = 'password_reset/pw_reset.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = self.request.POST.get("email")
        username = self.request.POST.get("username")
        firstname = self.request.POST.get("name")[:1]
        lastname = self.request.POST.get("name")[1:]
        if not models.Account.objects.filter(email=email).exists():
            email_error = "존재하지 않는 이메일입니다."
            return render(self.request, 'password_reset/pw_reset_fail.html', {"email_error": email_error})
        if not models.Account.objects.filter(username=username).exists():
            username_error = "존재하지 않는 아이디입니다."
            return render(self.request, 'password_reset/pw_reset_fail.html', {"username_error": username_error})
        if models.Account.objects.filter(email=email, username=username,
                                         first_name=firstname, last_name=lastname).exists():
            return super().form_valid(form)
        else:
            total_error = "이름을 다시 확인해주세요"
            return render(self.request, 'password_reset/pw_reset_fail.html', {"total_error": total_error})


class PWResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset/pw_reset_done.html'


class PWResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset/pw_reset_confirm.html'


class PWResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset/pw_reset_complete.html'

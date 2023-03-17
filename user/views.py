from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.db import transaction
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils import timezone
from . import models


def register(request):
    if request.method == "POST":
        print(request.POST)
        user_id = request.POST['userid']
        password = request.POST['password']
        user_email = request.POST['email']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        birth_date = request.POST['birthday']
        phone_number = request.POST['phone_number']
        postal_code = request.POST['postal_code']
        city = request.POST['city']
        address = request.POST['address']
        must_agree = request.POST['must_agree']
        option_agree = request.POST['option_agree']
        height = request.POST['height']
        weight = request.POST['weight']
        gender = request.POST['gender']
        profile_img = request.FILES.get('profile_img', None)
        # 파일 업로드 처리 - 중복 방지
        if profile_img:
            profile_img.name = f"{timezone.now().strftime('%Y%m%d_%H%M%S')}-{profile_img.name}"

        # 1. 데이터 유효성 검사
        try:
            validate_email(user_email)
            validate_password(password)
        except ValidationError as e:
            error_msg = "이메일 또는 패스워드 형식이 맞지 않습니다."
            return render(request, "register.html", {"error_msg": error_msg})

        # 2. DB 데이터 삽입
        with transaction.atomic():
            user = models.Account.objects.create_user(user_id, user_email, password, first_name=first_name,
                                                   last_name=last_name, birth_date=birth_date,
                                                   phone_number=phone_number)
            models.Address.objects.create(postal_code=postal_code, city=city, address=address or None, user=user)
            models.Option.objects.create(height=height or None, weight=weight or None, gender=gender or None,
                                             user=user)
            models.Agree.objects.create(must_agree=must_agree, option_agree=option_agree, user=user)
            models.ProfileImage.objects.create(profile_img=profile_img, user=user)

        user = authenticate(username=user_id, password=password)
        if user is not None:
            register_success = '회원 가입이 완료되었습니다. 로그인해주세요.'
            return render(request, 'login.html', {"register_success": register_success})

    return render(request, "register.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session['user_id'] = user.id
            # print(request.session)
            # print(user.id)
            return redirect('home')
        else:
            error_msg = "아이디 또는 비밀번호가 틀렸습니다."
            return render(request, "login.html", {"error_msg": error_msg})

    return render(request, "login.html")


# 아이디 찾기
def find_username(request):
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST['name'][:1]
        last_name = request.POST['name'][1:]
        birth_date = request.POST.get('birth_date')
        # print(request.POST)
        try:
            user = models.Account.objects.get(email=email, first_name=first_name, last_name=last_name,
                                           birth_date=birth_date)
            return render(request, 'find_username.html', {"find_id": user.username})
        except models.Account.DoesNotExist:
            error_msg = '등록 된 계정은 없습니다.'
            return render(request, 'find_username.html', {"error_msg": error_msg})

    return render(request, 'find_username.html')


def logout_page(request):
    logout(request)
    return redirect("home")


def naver_callback(request):
    return render(request, "naver_callback.html")

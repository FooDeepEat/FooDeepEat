from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . import models


def service(request):
    user_id = request.session.get('user_id')  # 세션 데이터에서 유저 ID 불러오기
    if user_id:
        user = models.User.objects.get(id=user_id)
        return render(request, "calorie/service.html", {'username': user.username})
    else:
        return redirect('login')


def mypage(request):
    user_id = request.session.get('user_id')  # 세션 데이터에서 유저 ID 불러오기
    if user_id:
        user = models.User.objects.get(id=user_id)
        return render(request, "calorie/mypage.html", {'username': user.username})
    else:
        return redirect('login')


def home(request):
    return render(request, "calorie/home.html")


def introduce(request):
    return render(request, "calorie/introduce.html")


# 아이디 찾기
def find_username(request):
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST['name'][:1]
        last_name = request.POST['name'][1:]
        birth_date = request.POST.get('birth_date')
        print(request.POST)
        try:
            user = models.User.objects.get(email=email, first_name=first_name, last_name=last_name,
                                           birth_date=birth_date)
            return render(request, 'users/find_username.html', {"find_id": user.username})

        except models.User.DoesNotExist:
            error_msg = '등록 된 계정은 없습니다.'
            return render(request, 'users/find_username.html', {"error_msg": error_msg})

    return render(request, 'users/find_username.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session['user_id'] = user.id
            print(request.session)
            print(user.id)
            return redirect('home')
        else:
            error_msg = "아이디 또는 비밀번호가 틀렸습니다."
            return render(request, "users/login.html", {"error_msg": error_msg})

    return render(request, "users/login.html")


def logout_page(request):
    logout(request)
    return redirect("home")


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

        # Insert SQL문 생성
        user = models.User.objects.create_user(user_id, user_email, password, first_name=first_name,
                                               last_name=last_name, birth_date=birth_date, phone_number=phone_number)
        address = models.UserAddress.objects.create(postal_code=postal_code, city=city, address=address or None,
                                                    user=user)
        option_info = models.UserOption.objects.create(height=height or None, weight=weight or None,
                                                       gender=gender or None, user=user)
        user_agree = models.UserAgree.objects.create(must_agree=must_agree, option_agree=option_agree, user=user)
        user_profile_img = models.UserProfileImage.objects.create(profile_img=profile_img, user=user)

        # DB 데이터 삽입
        user.save()
        address.save()
        option_info.save()
        user_agree.save()
        user_profile_img.save()

        user = authenticate(username=user_id, password=password)
        if user is not None:
            register_success = '회원 가입이 완료되었습니다. 로그인해주세요.'
            return render(request, 'users/login.html', {"register_success": register_success})

    return render(request, "users/register.html")

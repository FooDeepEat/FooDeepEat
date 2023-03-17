from django.shortcuts import render, redirect
from user import models
from . import models


def service(request):
    user_id = request.session.get('user_id')  # 세션 데이터에서 유저 ID 불러오기
    if user_id:
        user = models.Account.objects.get(id=user_id)
        return render(request, "service.html", {'username': user.username})
    else:
        return redirect('login')


def mypage(request):
    user_id = request.session.get('user_id')  # 세션 데이터에서 유저 ID 불러오기
    if user_id:
        user = models.Account.objects.get(id=user_id)
        return render(request, "mypage.html", {'username': user.username})
    else:
        return redirect('login')


def home(request):
    return render(request, "home.html")


def introduce(request):
    return render(request, "introduce.html")

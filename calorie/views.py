from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from . import models


@login_required
def service(request):
    user = request.user
    return render(request, "service.html", {"user": user})


@login_required
def mypage(request, date=None):
    if not date:
        today = datetime.now().date().strftime("%Y-%m-%d")
        # 날짜값이 있으면 앞, 없으면 today
        return redirect('mypage_with_date', date=today)

    if request.method == 'POST':
        edit_date = request.POST.get('edit_date')
        return redirect('mypage_with_date', date=edit_date)

    user = request.user
    memos = models.UserMemo.objects.filter(user_id=user.id, date=date)
    foods = models.UserFood.objects.filter(user_id=user.id, date=date)
    return render(request, "mypage.html", {"user": user, "memos": memos, "date": date, "foods": foods})


def home(request):
    return render(request, "home.html")


def introduce(request):
    return render(request, "introduce.html")

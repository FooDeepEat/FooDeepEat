from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . import models


@login_required
def mypage(request, date=None):
    user = request.user
    date = request.GET.get('date') or timezone.localdate().strftime("%Y-%m-%d")

    if request.method == 'POST':
        memo_text = request.POST.get('memo_text', '')

        if memo_text:
            memos, created = models.UserMemo.objects.get_or_create(user_id=user.id, date=date,
                                                                   defaults={'description': memo_text})
            if not created:
                memos.description = memo_text
                memos.save()
        else:
            memos = models.UserMemo.objects.filter(user_id=user.id, date=date).first()
            if memos:
                memos.delete()
        redirect('mypage_with_date', date=date)

    memos = models.UserMemo.objects.filter(user_id=user.id, date=date).first()
    foods = models.UserFood.objects.filter(user_id=user.id, date=date).first()
    return render(request, "mypage.html", {"user": user, "memos": memos, "date": date, "foods": foods})


@login_required
def service(request):
    user = request.user
    return render(request, "service.html", {"user": user})


def home(request):
    return render(request, "home.html")


def introduce(request):
    return render(request, "introduce.html")

from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . import models


@login_required
def service(request):
    user = request.user
    return render(request, "service.html", {"user": user})


@login_required
def mypage(request, date=None):
    user = request.user

    if not date:
        today = datetime.now().date().strftime("%Y-%m-%d")
        # URL 패턴 이름으로부터 URL 경로를 만들어주는 함수: reverse
        return redirect(reverse('mypage_with_date', kwargs={'date': today}))

    elif request.method == 'POST':
        edit_date = request.POST.get('edit_date')
        # print(edit_date)
        if not edit_date:
            edit_date = datetime.now().date().strftime("%Y-%m-%d")
        memo_text = request.POST.get('memo_text', '')
        # print(edit_date, memo_text)
        if memo_text:
            memos, created = models.UserMemo.objects.get_or_create(user=user, date=edit_date,
                                                                   defaults={'description': memo_text})
            if not created:
                memos.description = memo_text
                memos.save()
        else:
            memos = models.UserMemo.objects.filter(user_id=user.id, date=edit_date).first()
            if not memos:
                models.UserMemo.objects.filter(user=user, date=edit_date).delete()
        return redirect('mypage_with_date', date=edit_date)

    memos = models.UserMemo.objects.filter(user_id=user.id, date=date).first()
    foods = models.UserFood.objects.filter(user_id=user.id, date=date).first()
    return render(request, "mypage.html", {"user": user, "memos": memos, "date": date, "foods": foods})


def home(request):
    return render(request, "home.html")


def introduce(request):
    return render(request, "introduce.html")

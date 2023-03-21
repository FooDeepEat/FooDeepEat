from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
import random
from . import models


@login_required
def mypage(request, date=None):
    user = request.user
    date = request.GET.get('date') or timezone.localdate().strftime("%Y-%m-%d HH:MM:SS")

    if request.method == 'POST':
        memo_text = request.POST.get('memo_text', '')

        if memo_text:
            memos, created = models.UserMemo.objects.get_or_create(user_id=user.id, created_at=date,
                                                                   defaults={'description': memo_text})
            if not created:
                memos.description = memo_text
                memos.save()
        else:
            memos = models.UserMemo.objects.filter(user_id=user.id, created_at=date).first()
            if memos:
                memos.delete()
        redirect('calorie:mypage_with_date', date=date)

    memos = models.UserMemo.objects.filter(user_id=user.id, created_at=date).first()
    foods = models.UserFood.objects.filter(user_id=user.id, created_at=date).first()
    return render(request, "mypage.html", {"user": user, "memos": memos, "date": date, "foods": foods})


@login_required
def service(request):
    user = request.user

    if request.method == "POST":
        if request.GET.get('form') == "userfood":
            food_img = request.FILES.get('user_img', None)
        elif request.GET.get('form') == "usereaten":
            weight = request.POST["user_weight"]

        with transaction.atomic():
            models.UserFoodImage.objects.create(food_img=food_img, user=user)
            models.UserFood.objects.create(weight=weight, user=user)

    return render(request, "service.html")


def home(request):
    foods = models.Food.objects.all()
    random_food = random.choice(foods)
    food_img = models.FoodImage.objects.filter(name=random_food).all()
    if food_img:
        random_img = random.choice(food_img)
    else:
        random_img = None

    return render(request, "home.html", {"random_food": random_food, "random_img": random_img})


def introduce(request):
    return render(request, "introduce.html")

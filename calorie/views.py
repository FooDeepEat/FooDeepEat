from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
import random
from . import models


@login_required
def mypage(request, date=None):
    user = request.user
    date = request.GET.get('date') or timezone.localdate().strftime("%Y-%m-%d")

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

    food_img = None
    weight = None

    if request.method == "POST":
        if request.GET.get('form') == "userfood":
            food_img = request.FILES.get('user_img', None)
            if food_img:
                food_img.name = f"{user.username}.{food_img.name}"
        elif request.GET.get('form') == "usereaten":
            weight = request.POST["user_weight"]

        with transaction.atomic():
            if food_img:
                models.UserFoodImage.objects.create(food_img=food_img, user=user)
            if weight:
                models.UserFood.objects.create(weight=weight, user=user)

        user_foods = models.UserFood.objects.filter(user_id=user.id).all()
        user_food_img = models.UserFoodImage.objects.filter(name=user_foods).all()
        return render(request, "service.html", {"user_foods": user_foods, "user_food_img": user_food_img})

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


def search(request):
    food_name = request.GET.get('food_name')
    if food_name:
        # 검색어를 포함하는 음식 데이터 조회
        foods = models.Food.objects.filter(Q(name__icontains=food_name) | Q(description__icontains=food_name))
    else:
        foods = models.Food.objects.none()
    return render(request, "search.html", {"food_name": food_name, "foods": foods})


def introduce(request):
    return render(request, "introduce.html")

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import random
from django.core.paginator import Paginator
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

    if request.method == "POST":
        if request.GET.get('form') == "userfood":
            food_img = request.FILES.get('user_img', None)
            if food_img:
                food_img.name = f"{user.username}.{food_img.name}"
                models.UserFoodImage.objects.create(food_img=food_img, user=user)

        elif request.GET.get('form') == "usereaten":
            weight = request.POST["user_weight"]
            if weight:
                models.UserFood.objects.create(weight=weight, user=user)

        user_foods = models.UserFood.objects.filter(user_id=user.id).all()
        user_food_img = models.UserFoodImage.objects.filter(name=user_foods).all()
        return render(request, "service.html", {"user_foods": user_foods, "user_food_img": user_food_img})

    return render(request, "service.html")


def home(request):
    random_imgs = []
    foods = list(models.Food.objects.all())
    random_foods = random.sample(foods, 2)
    for random_food in random_foods:
        food_imgs = models.FoodImage.objects.filter(name=random_food).all()
        if food_imgs:
            random_img = random.choice(food_imgs)
        else:
            random_img = None
        random_imgs.append(random_img)

    random_food_list = zip(random_foods, random_imgs)

    return render(request, "home.html", {"random_food_list": random_food_list})


def search(request):
    food = request.GET.get('food')
    if food:
        # 검색어를 포함하는 음식 데이터 조회
        foods = models.Food.objects.filter(name__icontains=food).order_by('name').prefetch_related('images')
    else:
        foods = models.Food.objects.all().order_by('name').prefetch_related('images')

    # 한 페이지에 10개씩
    page_count = 10
    # foods를 페이징객체로 변환
    paginator = Paginator(foods, page_count)
    # 요청받은 페이지 번호 가져오기
    page = request.GET.get('page', 1)
    # 페이지에 해당하는 객체 반환
    paginated_foods = paginator.get_page(page)

    return render(request, "search.html", {"foods": paginated_foods})


def introduce(request):
    return render(request, "introduce.html")

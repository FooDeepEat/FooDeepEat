from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import random
from django.core.paginator import Paginator
from . import models
import requests
import base64
import time


@login_required
def mypage(request, date=None):
    user = request.user
    date = request.GET.get('date') or timezone.localdate().strftime("%Y-%m-%d")

    if request.method == 'POST':
        memo_text = request.POST.get('memo_text', '')
        print(memo_text)

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
        if 'user_food' in request.FILES:
            # 전송할 데이터 설정 (multipart/form-data 형태)
            user_foods = request.FILES.getlist('user_food')
            file_bytes_list = []
            for user_food in user_foods:
                file_bytes = user_food.read()  # 파일 내용을 바이너리로 읽어옴
                file_bytes_list.append(file_bytes)  # 바이너리를 바이트 리스트에 추가함
            # FastAPI 서버 URL 설정
            url = 'http://127.0.0.1:10000/cnn_model'
            uploaded_files = [('uploaded_files', file_bytes) for file_bytes in file_bytes_list]
            response = requests.post(url, files=uploaded_files)
            print(response)

            if response.status_code == 200:
            #     # FastAPI에서 반환한 JSON에서 이미지와 결과를 추출하고 저장
                image_with_results = None
                while True:
                    try:
                        image_with_results = response.json()
                        print("모델 분석 완료")
                        break
                    except:
            #             # 결과가 아직 도착하지 않았으면 1초 대기 후 다시 요청
                        time.sleep(1)
                        response = requests.post(url, files=uploaded_files)
                        continue
            #
                if image_with_results is not None:
                    for image_with_result in image_with_results:
                        food_img = image_with_result['image']
                        food_name = image_with_result['food_name']
                        user_name = user.first_name + user.last_name
        # #             # 바이너리 이미지를 디코딩
                        decoded_img = base64.b64decode(food_img)
        # #             # 이미지를 파일로 저장
                        with open(f'media/user_food/{user_name}-{food_name}-{timezone.now().date()}.jpg', 'wb') as f:
                            f.write(decoded_img)
                        print("사진 저장 완료")
                else:
                    print("이미지 없음")

        # elif request.GET.get('form') == "usereaten":
        #     weight = request.POST["user_weight"]
        #     if weight:
        #         models.UserFood.objects.create(weight=weight, user=user)
        #
        # user_foods = models.UserFood.objects.filter(user_id=user.id).all()
        # user_food_img = models.UserFoodImage.objects.filter(name=user_foods).all()
        # return render(request, "service.html", {"user_foods": user_foods, "user_food_img": user_food_img})

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

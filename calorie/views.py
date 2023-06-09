import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.db.models.functions import Round
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import random
from django.core.paginator import Paginator
from . import models
import requests
import base64
from django.core.files import File
from datetime import datetime
from django.db.models import Sum


@login_required
def mypage(request, date=None):
    user = request.user
    now = datetime.now(tz=None)
    date = request.GET.get('date') or now.strftime("%Y-%m-%d")

    if request.method == 'POST':
        if 'memo_text' in request.POST:
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

    food_date = datetime.strptime(date, '%Y-%m-%d')
    food_date = food_date.strftime('%Y-%m-%d')

    food_time = request.GET.get('food_time', '아침')

    memos = models.UserMemo.objects.filter(user_id=user.id, created_at=date).first()
    foods = models.UserFood.objects.filter(user_id=user.id,
                                           created_at__year=food_date[:4],
                                           created_at__month=food_date[5:7],
                                           created_at__day=food_date[8:10],
                                           user_food_time__food_time=food_time
                                           ).prefetch_related('user_food_images', 'user_food_time').all()

    if foods:
        time_nutri = foods.aggregate(energy=Round(Sum('energy'), 1),
                                     carbohydrate=Round(Sum('carbohydrate'), 1),
                                     protein=Round(Sum('protein'), 1),
                                     fat=Round(Sum('fat'), 1)
                                     )
    else:
        time_nutri = {
            'energy': 0,
            'carbohydrate': 0,
            'protein': 0,
            'fat': 0
        }

    today_foods = models.UserFood.objects.filter(user_id=user.id,
                                                 created_at__year=food_date[:4],
                                                 created_at__month=food_date[5:7],
                                                 created_at__day=food_date[8:10],
                                                 ).prefetch_related('user_food_images', 'user_food_time').all()

    if today_foods:
        today_nutri = today_foods.aggregate(energy=Round(Sum('energy'), 1),
                                            carbohydrate=Round(Sum('carbohydrate'), 1),
                                            protein=Round(Sum('protein'), 1),
                                            fat=Round(Sum('fat'), 1)
                                            )
    else:
        today_nutri = {
            'energy': 0,
            'carbohydrate': 0,
            'protein': 0,
            'fat': 0
        }

    created_at = models.UserFood.objects.filter(user_id=user.id,
                                                created_at__year=food_date[:4],
                                                created_at__month=food_date[5:7],
                                                created_at__day=food_date[8:10],
                                                user_food_time__food_time=food_time
                                                ).prefetch_related('user_food_images', 'user_food_time').first()

    return render(request, "mypage.html", {"user": user, "memos": memos, "date": date,
                                           "foods": foods, "time_nutri": time_nutri,
                                           "created_at": created_at, "food_time": food_time,
                                           "today_nutri": today_nutri})


@login_required
def service(request):
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

            if response.status_code == 200:
                # FastAPI에서 반환한 JSON에서 이미지와 결과를 추출하고 저장
                image_with_results = response.json()
                # print("모델 분석 완료")

                if image_with_results is not None:
                    user = request.user

                    user_food_list = []
                    for image_with_result in image_with_results:
                        # 음식 이름 가져오고 user_food 테이블에 저장하기
                        result_name = image_with_result['food_name']
                        food = models.Food.objects.filter(name=result_name).first()

                        # 음식 사진 가져오고 이미지 객체 변환
                        result_img = image_with_result['image']
                        user_name = user.first_name + user.last_name
                        # 바이너리 이미지를 디코딩
                        decoded_img = base64.b64decode(result_img)
                        # BytesIO 객체화
                        image_io = io.BytesIO(decoded_img)
                        # InMemoryUploadedFile 객체 생성(메모리에서 생성된 파일 객체)
                        now = datetime.now(tz=None)
                        image_file = InMemoryUploadedFile(image_io,
                                                          None,
                                                          f'{user_name}-'
                                                          f'{food.name}-'
                                                          f'{now.strftime("%Y-%m-%d")}.jpeg',
                                                          'image/jpeg',
                                                          image_io.getbuffer().nbytes,
                                                          None
                                                          )
                        # InMemoryUploadedFile 객체를 File 객체로 변환
                        image_file = File(image_file)

                        with transaction.atomic():
                            user_food_obj = models.UserFood.objects.create(user_id=user.id,
                                                                           name_id=food.id,
                                                                           weight=food.weight,
                                                                           energy=food.energy,
                                                                           carbohydrate=food.carbohydrate,
                                                                           protein=food.protein,
                                                                           fat=food.fat)
                            user_food_img_obj = models.UserFoodImage.objects.create(food_img=image_file,
                                                                                    name_id=user_food_obj.id)

                        confirm_food = {"image": user_food_img_obj.food_img, "user_food": user_food_obj, "food": food}
                        user_food_list.append(confirm_food)
                    return render(request, 'service.html', {"user_food_list": user_food_list})

        elif 'user_weight_1' in request.POST:
            # user = request.user
            for i in range(1, (len(request.POST) - 1) // 3 + 1):
                weight = request.POST.get(f"user_weight_{i}")
                created_at_str = request.POST.get(f"created_at_{i}")
                food_name = request.POST.get(f"food_name_{i}")
                # AM/PM 표시를 영어로 변환
                created_at_str = created_at_str.replace("오전", "AM").replace("오후", "PM")
                # # 문자열을 datetime 객체로 변환
                created_at_dt = datetime.strptime(created_at_str, '%Y년 %m월 %d일 %I:%M %p')
                # # datetime 객체를 원하는 형식의 문자열로 변환
                created_at_formatted = created_at_dt.strftime('%Y-%m-%d %H:%M:%S')

                food = models.Food.objects.filter(name=food_name).first()
                user_food = models.UserFood.objects.filter(
                    name_id=food.id,
                    created_at__year=created_at_formatted[:4],
                    created_at__month=created_at_formatted[5:7],
                    created_at__day=created_at_formatted[8:10],
                    created_at__hour=created_at_formatted[11:13],
                    created_at__minute=created_at_formatted[14:16],
                ).first()
                print(food.carbohydrate)
                print(food.protein)
                print(food.fat)
                print(food.energy)
                if user_food:
                    user_food.weight = weight
                    user_food.carbohydrate = f'{(food.carbohydrate * (float(weight) / 100)) * 4:.1f}'
                    user_food.protein = f'{(food.protein * (float(weight) / 100)) * 4:.1f}'
                    user_food.fat = f'{(food.fat * (float(weight) / 100)) * 9:.1f}'
                    user_food.energy = f'{float(user_food.carbohydrate)+float(user_food.protein)+float(user_food.fat):.1f}'
                    user_food.save()
                    food_time = request.POST.get('food_time')
                    models.UserFoodTime.objects.create(food_time=food_time, name_id=user_food.id)
                    print(user_food.carbohydrate)
                    print(user_food.protein)
                    print(user_food.fat)
                    print(user_food.energy)

            return redirect('calorie:mypage')

    return render(request, "service.html")


def home(request):
    random_imgs = []
    foods = list(models.Food.objects.all())
    if foods:
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
    else:
        return render(request, "home.html")


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

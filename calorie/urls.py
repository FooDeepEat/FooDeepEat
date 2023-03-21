from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views

app_name = "calorie"

urlpatterns = [
    # 첫 번째 URL 공간
    path('', views.home, name="home"),
    path('introduce/', views.introduce, name="introduce"),
    path('search/', views.search, name="search"),

    # 두 번째 URL 공간
    path('calorie/', include([
        path('', views.service, name='service'),
        path('mypage/', views.mypage, name='mypage'),
        path('mypage/<str:date>/', views.mypage, name='mypage_with_date'),
    ])),

    # static 파일을 서빙할수있는것을 지정하는것.
    # media_root에 지정한 폴더에서 취급하겠다.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

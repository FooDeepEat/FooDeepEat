from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # 첫 번째 URL 공간
    path('', views.home, name="home"),

    # 두 번째 URL 공간
    path('auth/', include([
        path("login/", views.login_page, name="login"),
        path("logout/", views.logout_page, name="logout"),
        path("register/", views.register, name="register"),
        path("find_username/", views.find_username, name="find_username"),
    ])),

    # 세 번째 URL 공간
    path('calorie/', include([
        path('', views.service, name='service'),
        path('mypage/', views.mypage, name='mypage'),
        path('introduce/', views.introduce, name="introduce"),
    ])),
    # static 파일을 서빙할수있는것을 지정하는것.
    # media_root에 지정한 폴더에서 취급하겠다.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

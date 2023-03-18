from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("register/", views.register, name="register"),
    path("find_username/", views.find_username, name="find_username"),

    # static 파일을 서빙할수있는것을 지정하는것.
    # media_root에 지정한 폴더에서 취급하겠다.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

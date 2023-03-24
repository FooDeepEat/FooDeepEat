from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
                  path("login/", views.LoginView.as_view(), name="login"),
                  path("logout/", views.logout_view, name="logout"),
                  path("register/", views.register, name="register"),
                  path("register/edit", views.register_edit, name="register_edit"),
                  path("find_username/", views.find_id, name="find_id"),
                  path('password_reset/', views.PWResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', views.PWResetDoneView.as_view(), name='password_reset_done'),
                  path('password_reset/confirm/<uidb64>/<token>/', views.PWResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('password_reset/complete/', views.PWResetCompleteView.as_view(),
                       name='password_reset_complete'),

                  # static 파일을 서빙할수있는것을 지정하는것.
                  # media_root에 지정한 폴더에서 취급하겠다.
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

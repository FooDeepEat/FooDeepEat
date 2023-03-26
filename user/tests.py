from django.test import TestCase

# Create your tests here.

# path('send_email/', views.send_email, name='send_email'),


# from django.core.mail.message import EmailMessage
#
# def send_email(request):
#     subject = "message"
#     to = ["ssd3784@gmail.com"]
#     from_email = "ssd3784@gmail.com"
#     message = "메세지 테스트"
#     EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()



# <!-- 파일도 form에서 다룰수 있게 해준다. enctype="multipart/form-data" -->
# 		<form method="POST" enctype="multipart/form-data">



# 사용자의 아이디, 이메일, 전화번호 등과 같은 속성과 유사한 비밀번호는 사용할 수 없음
#             UserAttributeSimilarityValidator(),
#             # 최소 길이 8 ~ 최대 길이 12
#             MinLengthValidator(8), MaxLengthValidator(12),
#             # 흔하게 사용하는 비밀번호 못만듬
#             CommonPasswordValidator(),
#             # 숫자로만 비밀번호 못만듬
#             NumericPasswordValidator(),
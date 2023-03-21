from django.test import TestCase

# Create your tests here.


# from food_deep_eat import settings
# from django.core.mail import send_mail
# import random

# 이메일 유효성 검사
# try:
#     validate_email(email)
# except ValidationError as e:
#     error_msg = "이메일 형식이 맞지 않습니다."
#     return render(request, "register.html", {"error_msg": error_msg})
#
# # 이메일 인증코드 발송 기능
# if request.POST.get('sendvalicode'):
#     subject = '푸디핏 회원가입 인증코드입니다.'
#     message = '인증코드: ' + str(random.randint(1000, 9999))
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, from_email, recipient_list)
#
# # 이메일 인증코드 확인
# if request.POST.get("checkvalidcode"):
#     valid_code = request.POST['emailcheck']
#     if valid_code == request.session.get('valid_code') and email == request.session.get('email'):
#         valid_message = "인증 성공"
#     else:
#         valid_message = "인증 실패"
#     return render(request, "register.html", {"error_msg": valid_message})
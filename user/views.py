from . import models
from . import forms
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = forms.RegistrationForm()
    return render(request, 'register.html', {'form': form})


# 아이디 찾기
def find_id(request):
    if request.method == "POST":
        email = request.POST["email"]
        first_name = request.POST['name'][:1]
        last_name = request.POST['name'][1:]
        birth_date = request.POST['birth_date']
        # print(request.POST)
        try:
            user = models.Account.objects.get(email=email, first_name=first_name, last_name=last_name,
                                              birth_date=birth_date)
            return render(request, 'find_id.html', {"find_id": user.username})
        except models.Account.DoesNotExist:
            error_msg = '등록 된 계정은 없습니다.'
            return render(request, 'find_id.html', {"error_msg": error_msg})

    return render(request, 'find_id.html')


class LoginView(LoginView):
    template_name = 'login.html'


def logout_view(request):
    logout(request)
    return redirect("calorie:home")

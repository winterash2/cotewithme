from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def signup(request):
    # HTTP Method가 POST 인 경우
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        # 모델폼의 유효성 검증이 valid할 경우, DB에 저장
        if signup_form.is_valid():
            signup_form.save()
        return redirect('main_page')

    # HTTP Method가 GET 인 경우
    else:
        signup_form = UserCreationForm()

    return render(request, 'registration/signup.html', {'signup_form': signup_form})
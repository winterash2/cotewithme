from django.shortcuts import render, redirect

# Create your views here.


def main_page(request):
    if( request.user.is_authenticated == True):
        return render(request, 'board/base.html', {})
    else:
        return redirect('login')


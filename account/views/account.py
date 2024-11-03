from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_moderator:
            return redirect('moderators:quiz_change_list')
        else:
            return redirect('respondents:quiz_list')
    return render(request, 'account/home.html')

def home_page(request) :
    logout(request)
    return render(request, 'account/home.html')

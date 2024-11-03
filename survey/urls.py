"""
URL configuration for survey project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin

from django.urls import include, path
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

from account.views import account, moderators, respondents


urlpatterns = [
    path('', include('account.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', account.SignUpView.as_view(), name='signup'),
    path('accounts/signup/respondent/', respondents.RespondentSignUpView.as_view(), name='respondent_signup'),
    path('accounts/signup/moderator/', moderators.ModeratorSignUpView.as_view(), name='moderator_signup'),
    path('accounts/logout', account.home_page, name='logout'),
    path('account/login', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

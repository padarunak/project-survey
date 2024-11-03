from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def respondent_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):

    '''
    Декоратор для представлений, который проверяет,
    является ли вошедший в систему пользователь респондентом,
    и при необходимости перенаправляет на страницу входа.
    '''

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_respondent,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def moderator_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Декоратор для представлений, который проверяет,
    является ли вошедший в систему пользователь модератором,
    и при необходимости перенаправляет на страницу входа.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_moderator,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

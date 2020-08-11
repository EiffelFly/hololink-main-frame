from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView)
from .views import sign_up, sign_up_with_account_password, sign_up_with_email, CustomLoginView, verify, sign_up_with_email_verification, sign_up_success, sign_up_verification_failed
from .forms import EmailValidationOnForgotPassword


# we use many built-in auth-related views from django.contrib.auth.urls
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    # we override this form class of this view
    path('password-reset/', PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('verification/<str:email>/<str:emailToken>/', verify, name='verify_user_token'), 
    path('verification/failed', sign_up_verification_failed, name='verify_user_token_failed') 
]

# some custom views
urlpatterns += [
    path('sign-up/', sign_up, name='sign_up'),
    path('sign-up/with-account-password/', sign_up_with_account_password, name='sign_up_with_account_password'), # not shown directly on web interface
    path('sign-up/sign-up-with-email/', sign_up_with_email_verification, name='sign_up_with_email'),
    path('sign-up/success', sign_up_success, name='sign_up_success'), 
] 


# Django imports
from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('login-profile/', views.login_success_view, name='login_done'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/', views.PasswordResetConfirmView.as_view, name='password_reset_confirm'),

    path('password-change', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # path('<slug:slug>/', view=views.user_detail.as_view(), name='user_detail') # Match a user name
]

"""django.contrib.auth.urls includes a lot of url patterns : 
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']"""
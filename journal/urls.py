from django.urls import path

from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('my-login/', views.my_login, name='my_login'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-thought/', views.create_thought, name='create_thought'),
    path('my-thoughts/', views.my_thoughts, name='my_thoughts'),
    path('update-thought/<str:pk>', views.upadate_thought, name='update_thought'), 
    path('delete-thought/<str:pk>', views.delete_thought, name='delete_thought'), 
    path('profile-management/', views.profile_management, name='profile_management'), 
    path('delete-account/', views.delete_account, name='delete_account'), 

    # Allow to enter email to receive a passwort reset link
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='journal/password-reset.html'), name='reset_password'),
    # show a success message after submitting the email
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='journal/password-reset-sent.html'), name='password_reset_done'),
    # send a link to reset the password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='journal/password-reset-form.html'), name='password_reset_confirm'),
    # show success message after resetting the password
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='journal/password-reset-complete.html'), name='password_reset_complete'),
]
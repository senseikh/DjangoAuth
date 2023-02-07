from django.urls import path
from . import views
from django.contrib.auth import views as django_auth_views

urlpatterns = [
    path('', views.log_in, name='accounts_home'),
    path('signup/', views.register, name='signup'),
    path('activate/<uidb64>/<token>/', views.verify_email_address,name='activate'),
    path('signin/', views.log_in, name='signin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/<str:username>/', views.user_profile, name='user_profile'),
    path('changepassword/', views.password_change, name='password_change'),
    path('resetpassword/', django_auth_views.PasswordResetView.as_view(template_name = 'accounts/requestpasswordreset.html'), name='password_reset'),
    path('resetpasswordsent/', django_auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/passwordresetsent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(template_name = 'accounts/resetpassword.html'), name='password_reset_confirm'),
    path('reset/done/', django_auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts/passwordresetdone.html'), name='password_reset_complete'),
    path('logout/', views.log_out, name='logout'),


    path('staffmembers/', views.staff_members, name='staff_members'),
    path('staffmembers/<int:id>', views.staff_details, name='staff_details'),
    path('staffmembers/<int:id>/delete', views.delete_staff, name='delete_staff'),
    path('staffmembers/<int:id>/deactivate', views.deactivate_staff, name='deactivate_staff'),
    path('staffmembers/<int:id>/activate', views.activate_staff, name='activate_staff')
]
from django.urls import path
from .views import index
from django.contrib.auth import views as auth_views

app_name = 'frontend'

urlpatterns = [
    #path('register/', views.register, name='register'),
    #path("login/", views.login_view, name="login"),
    #path('dashboard/', views.dashboard, name='dashboard'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    #path('reset_balance/', views.reset_balance, name='reset_balance'),
    #path('change_leverage/', views.change_leverage, name='change_leverage'),
    #path("referrals/", views.referrals, name="referrals"),
    path("", index, name="index")
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import RegisterView, BalanceView, ReferralsView, LeverageView, register

app_name = 'accounts'

urlpatterns = [
    # OLD path('register/', views.register, name='register'),
    path("login/", views.login_view, name="login"),
    # OLD path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('api/balance/', BalanceView.as_view(), name='balance'),
    # OLD path('change_leverage/', views.change_leverage, name='change_leverage'),
    path("api/register/", register, name="register"),
    path("api/Referral/", ReferralsView.as_view(), name="Referral"),
    path("api/leverage/", LeverageView.as_view(), name="leverage"),
]



from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import RegisterView, BalanceView, ReferralsView, LeverageView

app_name = 'accounts'

urlpatterns = [
    # OLD path('register/', views.register, name='register'),
    # OLD path("login/", views.login_view, name="login"),
    path("api/login/", auth_views.LoginView.as_view(), name="login"), # Not sure if this is correct.
    # OLD path('dashboard/', views.dashboard, name='dashboard'), # Need to figure out what to do with this. I think the Dashboard will function differently with React.
    # OLD path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path("api/logout/", auth_views.LogoutView.as_view(next_page='home'), name="logout"), # Not sure if this is correct.
    path('api/balance/', BalanceView.as_view(), name='balance'),
    # OLD path('change_leverage/', views.change_leverage, name='change_leverage'),
    #path("api/register/", RegisterView.as_view(), name="register"),
    path("api/Referral/", ReferralsView.as_view(), name="Referral"),
    path("api/leverage/", LeverageView.as_view(), name="leverage"),
]



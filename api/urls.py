from django.urls import path
from . import views
from accounts import views as accounts_views
from accounts import urls as accounts_urls
from accounts.views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('profiles/', views.UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/<int:pk>/', views.UserProfileDetail.as_view(), name='userprofile-detail'),
    path('market_data/time_series/<str:symbol>/', views.time_series_data, name='time_series_data'),
    path('orders/buy/', views.create_buy_order, name='create_buy_order'),
    path('orders/sell/', views.create_sell_order, name='create_sell_order'),
    path('equity/', views.get_equity, name='get_equity'),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]


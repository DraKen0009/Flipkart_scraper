from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api import views

urlpatterns = [
    path("register/", views.UserRegistrationAPIView.as_view(), name="create-user"),
    path("login/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("user/", views.UserAPIView.as_view(), name="user-info"),
    path('scrape/', views.DataApiView.as_view(), name='scrape'),

]

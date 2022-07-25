from django.urls import path
from .views import LogoutView, user_info, SignInAPIView

urlpatterns = [
    path('login/', SignInAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='api_token_delete'),
    path('user_info/', user_info)
]

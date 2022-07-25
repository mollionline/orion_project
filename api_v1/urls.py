from django.urls import path
from .views import LogoutView, user_info, SignInAPIView
from accounts.views import CreateUserAPIView, DeleteUserAPIView, UpdateUserAPIView, UserListAPIView

urlpatterns = [
    path('login/', SignInAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='api_token_delete'),
    path('user_info/', user_info),
    path('user/create', CreateUserAPIView.as_view(), name='create_user'),
    path('user/<int:pk>/delete', DeleteUserAPIView.as_view(), name='delete_user'),
    path('user/<int:pk>/update', UpdateUserAPIView.as_view(), name='update_user'),
    path('users/', UserListAPIView.as_view(), name='list_user')
]

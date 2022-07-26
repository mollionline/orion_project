from django.urls import path
from .views import (LogoutView, user_info, SignInAPIView,
                    CreateNodeAPIView, UpdateNodeAPIView,
                    NodesListAPIView, CreateDeviceAPIView,
                    DeleteDeviceAPIView, UpdateDeviceAPIView,
                    DevicesListAPIView, CreateMeterAPIView,
                    DeleteMeterAPIView, MeterListAPIView,
                    UpdateMeterAPIView, ApartmentFilterMeterAPIView,
                    DeviceFilterRangeDatesAPIView)
from accounts.views import CreateUserAPIView, DeleteUserAPIView, UpdateUserAPIView, UserListAPIView

urlpatterns = [
    path('login/', SignInAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='api_token_delete'),
    path('user_info/', user_info),
    path('user/create', CreateUserAPIView.as_view(), name='create_user'),
    path('user/<int:pk>/delete', DeleteUserAPIView.as_view(), name='delete_user'),
    path('user/<int:pk>/update', UpdateUserAPIView.as_view(), name='update_user'),
    path('users/', UserListAPIView.as_view(), name='list_user'),
    path('apartment/<int:pk>/node_create', CreateNodeAPIView.as_view(), name='node_apartment_create'),
    path('node/<str:uuid>/update', UpdateNodeAPIView.as_view(), name='node_update'),
    path('nodes/', NodesListAPIView.as_view(), name='list_node'),
    path('apartment/<int:pk>/device_create', CreateDeviceAPIView.as_view(), name='device_apartment_create'),
    path('device/<str:uuid>/delete', DeleteDeviceAPIView.as_view(), name='device_delete'),
    path('device/<str:uuid>/update', UpdateDeviceAPIView.as_view(), name='device_update'),
    path('devices/', DevicesListAPIView.as_view(), name='device_list'),
    path('device/<str:uuid>/meter_create', CreateMeterAPIView.as_view(), name='meter_create'),
    path('meter/<str:uuid>/delete', DeleteMeterAPIView.as_view(), name='meter_delete'),
    path('meters/', MeterListAPIView.as_view(), name='meter_list'),
    path('meter/<str:uuid>/update', UpdateMeterAPIView.as_view(), name='meter_update'),
    path('apartment_node/meter', ApartmentFilterMeterAPIView.as_view()),
    path('devices/date_range', DeviceFilterRangeDatesAPIView.as_view()), # этот вью не работает, к сожалению не разобралась как в поиск в
                                                                        # swagger дату задать и откуда брать показания устройств, с счетчиков?)
]

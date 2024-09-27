from django.urls import path, include
from. import views
from app_smart.API.viewsets import CreateUserAPIViewSet, SensorViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter 
from app_smart.API.viewsets import CSVUploadViewSet
from app_smart.views import CSVUploadFormView, process_csv_upload

# router = DefaultRouter()
# router.register(r'sensores', SensorViewSet)

router = DefaultRouter()
router.register(r'sensors', SensorViewSet)
router.register(r'upload-csv', CSVUploadViewSet, basename='upload-csv')



urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('api/create_user/', CreateUserAPIViewSet.as_view(), name='create_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/upload-csv/', CSVUploadFormView.as_view(), name='upload-csv'),
    path('process-upload/', process_csv_upload, name='process-upload'),
]
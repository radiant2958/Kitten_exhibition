from django.urls import path, include
from rest_framework import routers
from .views import BreedViewSet, KittenViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'breeds', BreedViewSet)
router.register(r'kittens', KittenViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # JWT авторизация
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

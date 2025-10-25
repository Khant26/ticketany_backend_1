from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import BannerViewSet, CategoryViewSet, EventViewSet, CustomerViewSet, OrderViewSet, TicketViewSet, custom_login

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'events', EventViewSet, basename='event')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', custom_login, name='custom_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
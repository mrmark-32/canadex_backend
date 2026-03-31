from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  ServiceViewSet, PortfolioViewSet, BlogPostViewSet, MenuItemViewSet

router = DefaultRouter()
router.register(r'menu', MenuItemViewSet, basename='menu')
router.register(r'services', ServiceViewSet)
router.register(r'portfolio', PortfolioViewSet)
router.register(r'blog', BlogPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
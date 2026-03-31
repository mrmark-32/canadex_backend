from rest_framework import viewsets
from .models import  Service, Portfolio, BlogPost,MenuItem
from .serializers import  ServiceSerializer, PortfolioSerializer, BlogPostSerializer, MenuItemSerializer

class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MenuItem.objects.filter(is_active=True).order_by('order')
    serializer_class = MenuItemSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'slug'         



class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    lookup_field = 'slug'


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(status='published').order_by('-published_at')
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
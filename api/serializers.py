from rest_framework import serializers
from .models import  Service, Portfolio, BlogPost, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['title', 'url', 'is_external', 'children']

    def get_children(self, obj):
        if obj.is_parent:
            return MenuItemSerializer(obj.children.filter(is_active=True).order_by('order'), many=True).data
        return []


class ServiceSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()
    detail_content = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'title', 'slug', 'short_para', 
            'image', 'feature1', 'feature2', 'feature3', 'feature4',
            'features', 'detail_content', 'created_at'
        ]

    def get_features(self, obj):
        return obj.features

    def get_detail_content(self, obj):
        return str(obj.detail_content) if obj.detail_content else ""

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return f"http://localhost:8000{obj.image.url}"
        return None
    


class PortfolioSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = [
            'id', 'title', 'slug', 'category', 'client', 'project_date',
            'image', 'short_description', 'description', 'technologies'
        ]

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return f"http://localhost:8000{obj.image.url}"
        return None
    


class BlogPostSerializer(serializers.ModelSerializer):
    featured_image = serializers.SerializerMethodField()
    og_image = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'category', 'meta_title', 'meta_description',
            'keywords', 'featured_image', 'og_image', 'short_description',
            'content', 'reading_time', 'published_at', 'created_at'
        ]

    def get_featured_image(self, obj):
        if obj.featured_image:
            return f"http://localhost:8000{obj.featured_image.url}"
        return None

    def get_og_image(self, obj):
        if obj.og_image:
            return f"http://localhost:8000{obj.og_image.url}"
        return obj.featured_image.url if obj.featured_image else None
from django.contrib import admin
from .models import  Service, Portfolio, BlogPost, MenuItem

# ==================== LISTING ADMIN ====================
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)

    fieldsets = (
        ('Menu Item', {
            'fields': ('title', 'url', 'parent', 'order', 'is_active', 'is_external')
        }),
    )


# ==================== SERVICE ADMIN ====================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'short_para_preview', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_para')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_para', 'image')
        }),
        ('Features (4 Separate Input Boxes)', {
            'fields': ('feature1', 'feature2', 'feature3', 'feature4'),
            'description': 'You can leave some blank if not needed.'
        }),
        ('Detail Page Content - Rich Text Editor', {
            'fields': ('detail_content',),
            'description': 'Write full formatted content here (headings, lists, bold, etc.)'
        }),
    )

    def short_para_preview(self, obj):
        return (obj.short_para[:80] + "...") if len(obj.short_para) > 80 else obj.short_para
    short_para_preview.short_description = "Short Description"




@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client', 'project_date', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'client', 'short_description')
    list_filter = ('category',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'category', 'client', 'project_date', 'image')
        }),
        ('Content', {
            'fields': ('short_description', 'description')
        }),
        ('Technologies', {
            'fields': ('technologies',),
            'description': 'Enter as JSON list e.g. ["Next.js", "Django", "Tailwind CSS"]'
        }),
    )



@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'published_at', 'reading_time')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'meta_description', 'keywords')
    list_filter = ('status', 'category')
    
    fieldsets = (
        ('SEO & Basic Info', {
            'fields': ('title', 'slug', 'category', 'meta_title', 'meta_description', 'keywords')
        }),
        ('Content', {
            'fields': ('short_description', 'content', 'featured_image', 'og_image')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at', 'reading_time')
        }),
    )
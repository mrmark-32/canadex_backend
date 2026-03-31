from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.utils import timezone

class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True, help_text="Leave empty for parent menu with dropdown")
    
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_external = models.BooleanField(default=False, help_text="Open in new tab")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title if not self.parent else f"{self.parent.title} > {self.title}"

    @property
    def is_parent(self):
        return self.children.exists()



class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    short_para = models.TextField(help_text="Short description shown on cards")
    
    # Real image upload
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    
    # 4 separate easy input boxes for features
    feature1 = models.CharField(max_length=200, blank=True)
    feature2 = models.CharField(max_length=200, blank=True)
    feature3 = models.CharField(max_length=200, blank=True)
    feature4 = models.CharField(max_length=200, blank=True)
    
    # ← CUSTOM RICH TEXT EDITOR (No more JSON!)
    detail_content = RichTextField(blank=True, null=True, 
                                   help_text="Write full detailed content here with formatting")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def features(self):
        feats = [self.feature1, self.feature2, self.feature3, self.feature4]
        return [f for f in feats if f.strip()]




class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    category = models.CharField(max_length=100, choices=[
        ('web', 'Web Development'),
        ('consulting', 'Consulting'),
        ('marketing', 'Digital Marketing'),
        ('design', 'UI/UX Design'),
        ('immigration', 'Immigration Services'),
        ('other', 'Other'),
    ])
    
    client = models.CharField(max_length=200, blank=True)
    project_date = models.DateField(blank=True, null=True)
    
    # Main featured image
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    
    # Short summary for cards
    short_description = models.TextField()
    
    # Full rich description
    description = RichTextField(blank=True, null=True)
    
    # Technologies / Tools used (comma separated or JSON)
    technologies = models.JSONField(default=list, blank=True, 
                                    help_text='Example: ["React", "Django", "Tailwind"]')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return self.technologies if isinstance(self.technologies, list) else []



class BlogPost(models.Model):
    STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published')]

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    category = models.CharField(max_length=100, choices=[
        ('business', 'Business & Consulting'),
        ('technology', 'Technology'),
        ('immigration', 'Immigration'),
        ('marketplace', 'Marketplace Tips'),
        ('canada', 'Canadian Life'),
        ('other', 'Other'),
    ])
    
    meta_title = models.CharField(max_length=250, blank=True, help_text="SEO Title (recommended 50-60 chars)")
    meta_description = models.TextField(blank=True, help_text="SEO Description (150-160 chars)")
    keywords = models.CharField(max_length=300, blank=True, help_text="Comma separated keywords")
    
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    og_image = models.ImageField(upload_to='blog/og/', blank=True, null=True, help_text="Open Graph image (1200x630 recommended)")
    
    short_description = models.TextField(help_text="Used in cards and meta")
    content = RichTextField()
    
    reading_time = models.PositiveIntegerField(default=0, help_text="In minutes (auto-calculated if left 0)")
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto calculate reading time (approx 200 words per minute)
        if self.reading_time == 0 and self.content:
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / 200))
        
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
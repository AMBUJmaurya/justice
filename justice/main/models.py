from django.db import models
from django.utils.text import slugify


class ContactInquiry(models.Model):
    SERVICE_CHOICES = [
        ('', 'Select a Service'),
        ('family', 'Family Law'),
        ('criminal', 'Criminal Law'),
        ('civil', 'Civil Law'),
        ('corporate', 'Corporate Law'),
        ('real-estate', 'Real Estate Law'),
        ('employment', 'Employment Law'),
        ('other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200)
    service = models.CharField(max_length=30, choices=SERVICE_CHOICES, blank=True)
    message = models.TextField()
    terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"


class PracticeArea(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    short_description = models.CharField(max_length=220, blank=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=80, blank=True)
    image_url = models.URLField(blank=True)
    case_count = models.PositiveIntegerField(default=0)
    show_on_home = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:140]
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=80, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    author_name = models.CharField(max_length=80, blank=True, default="Admin")
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

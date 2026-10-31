from django.contrib import admin

from .models import BlogPost, ContactInquiry, PracticeArea


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'service', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    list_filter = ('service', 'created_at')


@admin.register(PracticeArea)
class PracticeAreaAdmin(admin.ModelAdmin):
    list_display = ("title", "case_count", "show_on_home", "order", "is_active", "updated_at")
    list_filter = ("is_active", "show_on_home")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author_name", "published_at", "is_published", "updated_at")
    list_filter = ("is_published", "category")
    search_fields = ("title", "excerpt", "content", "author_name")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"

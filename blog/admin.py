from django.contrib import admin
from .models import Post, Comment, Category, Tag, Profile
from django.utils.html import format_html
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','publish','status', 'image_tag']
    list_filter = ['status','created','publish','author']
    search_fields = ['title','body']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ['author']
    date_hierarchy_fields = 'publish'
    ordering = ['status','publish']
    readonly_fields = ['image_tag']
    featured = ['featured']

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'body', 'publish', 'status', 'image', 'image_tag', 'tags', 'featured')
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" style="object-fit:cover; border-radius:6px;"/>', obj.image.url)
        return ""
    image_tag.short_description = 'Imagen'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','post','created','active']
    list_filter = ['active','created','updated']
    search_fields = ['name','email','body']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'twitter', 'github', 'linkedin')
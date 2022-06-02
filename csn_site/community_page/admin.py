from django.contrib import admin
from .models import Post, Photo, Tag

# Register your models here.
class PhotoInline(admin.TabularInline):
    model = Photo

class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
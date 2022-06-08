from django.contrib import admin
from .models import Post, Tag
# from .models import Photo

# Register your models here.
# class PhotoInline(admin.TabularInline):
#     model = Photo

# class PostAdmin(admin.ModelAdmin):
#     inlines = [PhotoInline, ]

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Post)
# admin.site.register(PostAdmin)
admin.site.register(Tag, TagAdmin)
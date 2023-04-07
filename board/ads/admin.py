from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Reply
from django_summernote.admin import SummernoteModelAdmin

class blogadmin(SummernoteModelAdmin):
    # displaying posts with title slug and created time
    list_display = ('title', 'text')
    list_filter = ("time_in", )
    search_fields = ['title', 'text']
    # prepopulating slug from title
    prepopulated_fields = {'text': ('title', )}
    summernote_fields = ('text', )

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, blogadmin)
admin.site.register(PostCategory)
admin.site.register(Reply)

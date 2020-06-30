from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['hash', 'name', 'from_url_shortcut',
                    'content_shortcut', 'created_by', 'created_at', ]

    # We don't display all the from_url
    def from_url_shortcut(self, obj):
        if len(obj.from_url) > 64:
            return f'{obj.from_url[:64]} ...'
        else:
            return obj.from_url

    # We don't display all the content
    def content_shortcut(self, obj):
        if len(obj.content) > 32:
            return f'{obj.content[:32]} ...'
        else:
            return obj.content


admin.site.register(Article, ArticleAdmin)

from django.contrib import admin
from .models import Article
from .models import Highlight


    

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['name', 'hash', 'from_url_shortcut',
                    'content_shortcut', 'created_by', 'created_at']

    filter_horizontal = ('projects', 'owned_by')
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




class HighlightAdmin(admin.ModelAdmin):
    list_display = ['highlighted_at', 'created_at', 'highlighted_words']
    filter_horizontal = ('highlighted_by',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Highlight, HighlightAdmin)
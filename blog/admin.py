from django.contrib import admin
from .models import Article, Comment

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Comment)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)

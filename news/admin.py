from django.contrib import admin

from news.models import Category, News, Comment, Customer

admin.site.register(Category)

class AdminNews(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_date')
admin.site.register(News, AdminNews)

class AdminComment(admin.ModelAdmin):
    list_display = ('comment', 'name', 'news')
admin.site.register(Comment, AdminComment)

admin.site.register(Customer)

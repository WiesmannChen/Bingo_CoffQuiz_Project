from django.contrib import admin
from coffquiz.models import Coffee, Article, Comment, UserProfile, LikeCoffee

class CoffeeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title', 'coffee', 'writer')

admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(LikeCoffee)

from django.contrib import admin
from .models import Store, MenuCategory, Menu, MenuOptionCategory, MenuOption

admin.site.register(Store)

class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'store']
admin.site.register(MenuCategory, MenuCategoryAdmin)

class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'store', 'category']
admin.site.register(Menu, MenuAdmin)

class MenuOptionCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'store']
admin.site.register(MenuOptionCategory, MenuOptionCategoryAdmin)

class MenuOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'store', 'category']
admin.site.register(MenuOption, MenuOptionAdmin)
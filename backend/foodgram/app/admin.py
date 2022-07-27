from django.contrib import admin

from . import models


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_editable = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'cooking_time')
    list_editable = ('author', 'name', 'cooking_time')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(models.Follow, FollowAdmin)

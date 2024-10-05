from django.contrib import admin
from .models import Breed, Kitten, Rating

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ('user', 'score')

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Kitten)
class KittenAdmin(admin.ModelAdmin):
    list_display = ('id', 'breed', 'color', 'age', 'owner', 'average_rating')
    list_filter = ('breed', 'color', 'age')
    search_fields = ('breed__name', 'color', 'description', 'owner__username')
    readonly_fields = ('average_rating',)
    inlines = [RatingInline]

    def average_rating(self, obj):
        return obj.get_average_rating()

    average_rating.short_description = 'Средний рейтинг'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'kitten', 'user', 'score')
    list_filter = ('score',)
    search_fields = ('kitten__breed__name', 'kitten__color', 'user__username')

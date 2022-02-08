from django.contrib import admin
from jedzonko.models import Recipe, Plan, RecipePlan, DayName, Page


class RecipePlanAdmin(admin.ModelAdmin):
    list_display = ('day_name', 'meal_name', 'recipe', 'plan')


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


admin.site.register(Recipe)
admin.site.register(Plan, PlanAdmin)
admin.site.register(RecipePlan, RecipePlanAdmin)
admin.site.register(DayName)
admin.site.register(Page)

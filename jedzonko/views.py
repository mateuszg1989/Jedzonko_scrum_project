from datetime import datetime
from jedzonko.models import Recipe
from django.shortcuts import render
from django.views import View
from random import shuffle

class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class LandingPageView(View):

    def get(self, request):
        recipe = list(Recipe.objects.all())
        shuffle(recipe)
        return render(request, "index.html", {'recipe': recipe})


class DashboardView(View):

    def get(self, request):
        recipes_number = Recipe.objects.count()

        return render(request, "dashboard.html", {'recipes_number': recipes_number})


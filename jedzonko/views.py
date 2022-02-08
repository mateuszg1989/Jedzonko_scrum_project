from datetime import datetime
from jedzonko.models import Recipe, Plan, Page
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from random import shuffle
from jedzonko.forms import RecipeForm, PlanForm
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist




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
        plan_number = Plan.objects.count()

        return render(request, "dashboard.html", {'recipes_number': recipes_number, 'plan_number': plan_number})
        last_added_plan = Plan.objects.all().order_by('created')[0]
        return render(request, "dashboard.html", {
            'recipes_number': recipes_number, 'plan_number': plan_number, 'last_added_plan': last_added_plan
                                                  })


class AddRecipeView(View):
    def get(self, request):
        form = RecipeForm()
        return render(request, 'app-add-recipe.html', {'form': form})

    def post(self, request):
        form = RecipeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            preparation_time = form.cleaned_data['preparation_time']
            ingredients = form.cleaned_data['ingredients']

            Recipe.objects.create(
                name=name,
                description=description,
                preparation_time=preparation_time,
                ingredients=ingredients)

            return redirect('/recipe/list')
        else:
            return render(request, 'app-add-recipe.html', {'form': form})


class RecipeListView(ListView):
    model = Recipe
    template_name = 'app-recipes.html'
    context_object_name = 'recipe'
    paginate_by = 50
    queryset = Recipe.objects.all().order_by('created').order_by('-votes')


class RecipeView(View):
    def get(self, request):
        return render(request, 'app-recipe-details.html')


class RecipeModifyView(View):
    def get(self, request):
        return render(request, 'app-edit-recipe.html')


class PlanListView(ListView):
    model = Plan
    template_name = 'app-schedules.html'
    context_object_name = 'plan'
    paginate_by = 50
    queryset = Plan.objects.all().order_by('name')


class PlanView(View):
    def get(self, request):
        return render(request, 'app-details-schedules.html')


class AddPlanView(View):
    def get(self, request):
        form = PlanForm()
        return render(request, 'app-add-schedules.html', {'form': form})

    def post(self, request):
        form = PlanForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            Plan.objects.create(
                name=name,
                description=description)
            return redirect('/plan/<id>/details')
        else:
            return render(request, 'app-add-schedules.html', {'form': form})



class AddRecipeToPlanView(View):
    def get(self, request):
        return render(request, 'app-schedules-meal-recipe.html')


class ContactView(View):
    def get(self, request):
        try:
            contact = Page.objects.get(slug='contact')
            return render(request, 'app-contact.html', {'contact': contact})
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/#contact')


class AboutView(View):
    def get(self, request):
        try:
            about = Page.objects.get(slug='about')
            return render(request, 'app-about.html', {'about': about})
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/#about')




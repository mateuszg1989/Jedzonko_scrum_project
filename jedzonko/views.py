from datetime import datetime
from jedzonko.models import Recipe, Plan, Page, RecipePlan, DayName
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from random import shuffle
from jedzonko.forms import RecipeForm, PlanForm, SchedulesMeatRecipeForm
from django.http import HttpResponse, HttpResponseRedirect
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
        plans = Plan.objects.all().order_by('-created')
        plan = plans[0]
        recipeplan = RecipePlan.objects.filter(plan_id=plan.id).order_by('order')
        daynames = DayName.objects.filter(id__in=recipeplan.values('day_name')).order_by('order')

        return render(request, "dashboard.html", {
            'recipes_number': recipes_number, 'plan_number': plan_number,
            'plan': plan, 'daynames': daynames, 'recipes': recipeplan
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
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        try:
            method_of_preparing = recipe.method_of_preparing.split('-')
        except Exception:
            method_of_preparing = recipe.method_of_preparing
        try:
            ingredients = recipe.ingredients.split('-')
        except Exception:
            ingredients = recipe.ingredients
        return render(request, 'app-recipe-details.html', {
            'recipe': recipe, 'ingredients': ingredients,
            'method_of_preparing': method_of_preparing
        })

    def post(self, request, id):
        if request.POST.get('voteup') == '+1':
            recipe = Recipe.objects.get(id=request.POST.get('id'))
            recipe.votes += 1
            recipe.save()
            return redirect(f'/recipe/{recipe.id}/')
        elif request.POST.get('votedown') == '-1':
            recipe = Recipe.objects.get(id=request.POST.get('id'))
            recipe.votes -= 1
            recipe.save()
            return redirect(f'/recipe/{recipe.id}/')


class RecipeModifyView(View):
    def get(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            return render(request, 'app-edit-recipe.html', {'recipe': recipe})
        except ObjectDoesNotExist:
            return HttpResponse('Błąd 404: przepis nie istnieje!')

    def post(self, request, recipe_id):
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        method_of_preparing = request.POST.get('method_of_preparing')
        if name != "" and ingredients != "" and description != "" and preparation_time != "" \
                and method_of_preparing != "":
            Recipe.objects.create(name=name, ingredients=ingredients, description=description,
                                  preparation_time=preparation_time, method_of_preparing=method_of_preparing)
            return HttpResponseRedirect('/recipe/list')
        else:
            return render(request, 'app-edit-recipe.html', {'alert_flag': True})


class PlanListView(ListView):
    model = Plan
    template_name = 'app-schedules.html'
    context_object_name = 'plan'
    paginate_by = 50
    queryset = Plan.objects.all().order_by('name')


class PlanView(View):
    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        recipe_plan = RecipePlan.objects.filter(plan_id=id).order_by('plan')
        day_name = DayName.objects.filter(id__in=recipe_plan.values('day_name')).order_by('order')
        return render(request, 'app-details-schedules.html',
                      {
                          'recipe_plan': recipe_plan,
                          'plan': plan,
                          'day_name': day_name,
                      })


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
            return redirect('plan/list/')
        else:
            return render(request, 'app-add-schedules.html', {'form': form})


class AddRecipeToPlanView(View):
    def get(self, request):
        form = SchedulesMeatRecipeForm()
        return render(request, 'app-schedules-meal-recipe.html', {'form': form})

    def post(self, request):
        form = SchedulesMeatRecipeForm(request.POST)
        if form.is_valid():
            select_plan = form.cleaned_data['select_plan']
            select_recipe = form.cleaned_data['select_recipe']
            meal_name = form.cleaned_data['meal_name']
            meal_order = form.cleaned_data['meal_order']
            day = form.cleaned_data['day']

            RecipePlan.objects.create(
                plan=select_plan,
                recipe=select_recipe,
                order=meal_order,
                meal_name=meal_name,
                day_name=day
            )
            return redirect(f'/plan/{select_plan.id}')
        else:
            return render(request, 'app-schedules-meal-recipe.html', {'form', form})


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

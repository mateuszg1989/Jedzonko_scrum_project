"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from jedzonko.views import IndexView, LandingPageView, DashboardView, AddRecipeView, RecipeListView, RecipeView, \
    RecipeModifyView, PlanView, AddPlanView, AddRecipeToPlanView, PlanListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('main/', DashboardView.as_view(), name='dashboard'),
    path('recipe/list/', RecipeListView.as_view(), name='recipes'),
    path('recipe/<int:id>/', RecipeView.as_view(), name='recipe'),
    path('recipe/add', AddRecipeView.as_view(), name='add-recipe'),
    path('recipe/modify/<int:id>', RecipeModifyView.as_view(), name='modify-recipe'),
    path('plan/list/', PlanListView.as_view(), name='plans'),
    path('plan/<int:id>', PlanView.as_view(), name='plan'),
    path('plan/add', AddPlanView.as_view(), name='add-plan'),
    path('plan/add-receipe', AddRecipeToPlanView.as_view(), name='add-recipe-to-plan')
]

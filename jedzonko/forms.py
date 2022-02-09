import django.forms as forms
from jedzonko.models import Recipe, Plan

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name','preparation_time','description','ingredients','method_of_preparing']
        labels = {
            'name': ('Nazwa przepisu'),
            'description':('Opis przepisu'),
            'preparation_time':('Czas przygotowania'),
            'ingredients':('Składniki'),
            'method_of_preparing':('Opis przygotowania'),
        }

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields =['name', 'description']
        labels = {
            'name': ('Nazwa planu'),
            'description': ("Opis")
        }

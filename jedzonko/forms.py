import django.forms as forms
from jedzonko.models import Recipe, Plan, DayName

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

class SchedulesMeatRecipeForm(forms.Form):

    select_plan = forms.ModelChoiceField(
        label='Wybierz plan',
        queryset=Plan.objects.all().order_by('name'),
        empty_label=None,
        widget=forms.Select
    )
    meal_name = forms.CharField(max_length=128, label='Nazwa posiłku')
    meal_order = forms.IntegerField(min_value=1, label='Numer posiłku')
    select_recipe = forms.ModelChoiceField(
        label='Przepis',
        queryset=Recipe.objects.all().order_by('name'),
        empty_label=None,
        widget=forms.Select,
    )
    day = forms.ModelChoiceField(
        label='Dzień',
        queryset=DayName.objects.all().order_by('id'),
        empty_label=None,
        widget=forms.Select,
    )
import django.forms as forms
from jedzonko.models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name','preparation_time','description','ingredients']
        labels = {
            'name': ('Nazwa przepisu'),
            'description':('Opis przepisu'),
            'preparation_time':('Czas przygotowania'),
            'ingredients':('Składniki')
        }

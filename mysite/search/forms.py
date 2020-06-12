from django import forms

from recipes.models import Rating, Ingredient

CHOICES = [
    (1, 'Very poor'),
    (2, 'Poor'),
    (3, 'Fine'),
    (4, 'Good'),
    (5, 'Excellent'),
]


class Add_ingredient(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['Ingredient_name', 'Ingredient_amount']
        widgets = {
            'ingredient_name': forms.TextInput(attrs={
                'id': 'Ingredient_name',
                'required': True,
                'placeholder': 'Add ingredient'
            }),
            'ingredient_amount': forms.TextInput(attrs={
                'id': 'Ingredient_amount',
                'required': True,
                'placeholder': 'Add amount'
            })
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        # exclude = ['author', 'updated', 'created', ]
        fields = ['comment', 'stars']
        widgets = {
            'comment': forms.TextInput(attrs={
                'id': 'ingredient-name',
                'required': True,
                'placeholder': 'Say something...'
            }),
            'stars': forms.NumberInput(attrs={
                'id': 'post-stars',
                'required': True

            }), }

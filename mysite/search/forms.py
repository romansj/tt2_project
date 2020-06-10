from django import forms

from recipes.models import Rating

CHOICES = [
    (1, 'Very poor'),
    (2, 'Poor'),
    (3, 'Fine'),
    (4, 'Good'),
    (5, 'Excellent'),
]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        # exclude = ['author', 'updated', 'created', ]
        fields = ['comment', 'stars']
        widgets = {
            'comment': forms.TextInput(attrs={
                'id': 'post-text',
                'required': True,
                'placeholder': 'Say something...'
            }),
            'stars': forms.NumberInput(attrs={
                'id': 'post-stars',
                'required': True

            }), }

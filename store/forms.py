from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):   # Capital M
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']

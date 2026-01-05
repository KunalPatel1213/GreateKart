from django import forms
from .models import ReviewRating
class ReviewForm(forms.modelForm):
    class Meta:
        model=ReviewRating
        fields=['subject', 'review', 'rating']
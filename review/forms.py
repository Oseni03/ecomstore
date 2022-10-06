from django import forms

from .models import Review

class ReviewForm(forms.ModelForm):
  name = forms.CharField(
    max_length=150, help_text="Required", 
    error_messages = {"required": "Please, enter your name"})
  email = forms.EmailField(
    max_length=150, help_text="Required", 
    error_messages = {"required": "Please, enter your email"})
  
  class Meta:
    model = Review
    fields = ["name", "email", "rating", "content"]
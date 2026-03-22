from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class TaskForm(forms.ModelForm):
    class Meta:
        from .models import Task
        model = Task
        fields = ["title", "description", "priority", "estimated_days", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "estimated_days": forms.NumberInput(attrs={"class": "form-control"}),
        }
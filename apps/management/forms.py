from django import forms
from .models import Department, Position, UnitNumber

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['unit', 'name', 'description']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Optional Description', 'rows': 3}),
        }

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['department', 'name', 'description']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Optional Description', 'rows': 3}),
        }

class UnitNumberForm(forms.ModelForm):
    class Meta:
        model = UnitNumber
        fields = ['city', 'unit_no', 'description']
        widgets = {
            'city': forms.Select(attrs={'class': 'form-select'}),
            'unit_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dhaka-01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Optional Description', 'rows': 3}),
        }

from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'category', 'course', 'level', 'file']


class BookFormCleared(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'category', 'course', 'level', 'file', 'cleared']
        widgets = {
            'cleared': forms.CheckboxInput(),
        }



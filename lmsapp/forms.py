from django import forms
from .models import BookLending

class BookLendingForm(forms.ModelForm):
    class Meta:
        model = BookLending
        fields = [ 'book', 'lending_time']
        widgets = {
            'book': forms.Select(attrs={'class': 'select2-ajax'}),
            'lending_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

from django import forms
from .models import BookLending,Book

class BookLendingForm(forms.ModelForm):
    class Meta:
        model = BookLending
        fields = [ 'book', 'lending_time']
        widgets = {
            'book': forms.Select(attrs={'class': 'select2-ajax'}),
            'lending_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(AllowLend=True)
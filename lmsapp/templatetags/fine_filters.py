from django import template
from datetime import timedelta
from ..models import BookLending

register = template.Library()

@register.filter
def calculate_fine(book_lending):
    if book_lending.return_time and book_lending.return_time > book_lending.expected_return_date:
        days_overdue = (book_lending.return_time - book_lending.expected_return_date).days
        book = BookLending.objects.get(book=book_lending)
        book.fine_amount = fine_amount
        book.save()
        fine_amount = days_overdue * 7  # Assuming fine rate of 7 rupees per day
        return fine_amount
    else:
        return "No Fine"

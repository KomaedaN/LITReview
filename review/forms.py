from django import forms
from . import models


class TicketForm(forms.ModelForm):
    title = forms.CharField(max_length=128, label='Title',
                            widget=forms.TextInput(attrs={'class': "create_ticket_forms create_ticket_forms_title"}))

    description = forms.CharField(max_length=2048, label='Description',
                                  widget=forms.Textarea(attrs={'class': "create_ticket_forms"}))

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    RATING_CHOICE = [
        ("0", 0), ("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5),
    ]
    headline = forms.CharField(max_length=128, label='Title',
                            widget=forms.TextInput(attrs={'class': "create_ticket_forms create_ticket_forms_title"}))

    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=RATING_CHOICE,)

    body = forms.CharField(max_length=2048, label='Description',
                           widget=forms.Textarea(attrs={'class': "create_ticket_forms"}))

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']

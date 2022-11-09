from django import forms
from . import models
from authentication.models import UserFollows

class TicketForm(forms.ModelForm):
    title = forms.CharField(max_length=128, label='Titre',
                            widget=forms.TextInput(attrs={'class': "create_ticket_forms create_ticket_forms_title"}))

    description = forms.CharField(max_length=2048, label='Description',
                                  widget=forms.Textarea(attrs={'class': "create_ticket_forms"}))

    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    RATING_CHOICE = [
        ("0", 0), ("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5),
    ]
    headline = forms.CharField(max_length=128, label='Note',
                               widget=forms.TextInput(attrs={'class': "create_ticket_forms create_ticket_forms_title"}))

    rating = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': "ul_review"}), choices=RATING_CHOICE, )

    body = forms.CharField(max_length=2048, label='Commentaire',
                           widget=forms.Textarea(attrs={'class': "create_ticket_forms"}))

    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']


class DeleteContentForm(forms.Form):
    delete_content = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']

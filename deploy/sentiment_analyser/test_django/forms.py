from django import forms


class UserForm(forms.Form):
    review = forms.CharField(label='Your review', widget=forms.Textarea)

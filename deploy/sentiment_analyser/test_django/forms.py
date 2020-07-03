from django import forms


class UserForm(forms.Form):
    review = forms.CharField(label='Отзыв', widget=forms.Textarea)

from django import forms

class FormData(forms.Form):
    email_content = forms.CharField(max_length=5000, required=True)
from django import forms

class UploadPictureForm(forms.Form):
    title = forms.CharField(max_length=50)
    img = forms.ImageField()
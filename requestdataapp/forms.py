from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms.widgets import Textarea


class UserBioForm(forms.Form):
    name = forms.CharField(max_length=50)
    age = forms.IntegerField(label='My age', max_value=100, min_value=10)
    bio = forms.CharField(label='Biography', widget=Textarea)

def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError('file name should not contain "virus"')

class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])
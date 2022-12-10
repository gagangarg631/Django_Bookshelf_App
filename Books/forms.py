from django import forms

class AddBookForm(forms.Form):
    sPdf = forms.FileField(error_messages={'required': 'upload file','missing': 'file missing'})
    sName = forms.CharField(error_messages={'required': 'Please enter book name'},strip=True)
    sAllTags = forms.CharField()
    

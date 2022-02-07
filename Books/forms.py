from django import forms

class AddBookForm(forms.Form):
    sPdf = forms.FileField(error_messages={'required': 'upload pdf file','missing': 'Pdf file missing'})
    sName = forms.CharField(error_messages={'required': 'Please enter book name'},strip=True)
    sAllTags = forms.CharField()
    

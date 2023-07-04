from django import forms
class inputForm(forms.Form): 
    input = forms.FileField(required = True )
    
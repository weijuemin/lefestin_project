from django import forms

class UploadFileForm(forms.Form):
    image = forms.FileField()

class UploadGroupImg(forms.Form):
	GroupImage = forms.FileField()
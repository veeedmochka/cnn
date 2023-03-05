from django import forms

from user.models import UserImage


class FileForm(forms.ModelForm):
    
    class Meta:
        model = UserImage
        fields = ('title', 'image')

        widgets = {
            'image': forms.FileInput(attrs={'class': 'from-control', 'id': 'image'}),
            'title': forms.TextInput(attrs={'style': 'display: none;'})
        }

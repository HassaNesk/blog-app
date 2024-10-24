from typing import Any
from django import forms

from blog.models import Post, Comment


class AcountForm(forms.Form):
    gender_choice = (('آقا' , "آقا"),("خانم",'خانم'))
    first = forms.CharField(max_length=50,required=True)
    last = forms.CharField(max_length=50,required=True)
    gender = forms.ChoiceField( choices=gender_choice , widget=forms.RadioSelect)
    # phone = forms.CharField(max_length=11 , blank=True)
    address = forms.CharField(max_length=250,widget=forms.Textarea,required=False)
    age = forms.IntegerField(min_value=0)
    
    def clean_age(self):
        a= self.cleaned_data['age']
        if a > 100:
            raise forms.ValidationError('پیر سگ')
        return a
    

   
        
class ContactForm(forms.Form):
    name = forms.CharField(max_length=250,required=True)
    message = forms.CharField(max_length=250,widget=forms.Textarea,required=True)
    subject = forms.CharField(max_length=250,required=True)
    email = forms.EmailField(max_length=250,required=True)
    phone = forms.CharField(max_length=11,widget=forms.Textarea,required=False)


class ShareForm(forms.Form):
    name = forms.CharField(max_length=250,required=True)
    message = forms.CharField(max_length=250,widget=forms.Textarea,required=True)
    to = forms.EmailField(max_length=250,required=True)




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name' , 'body',]

class loginForm(forms.Form):
    username = forms.CharField(max_length=250,required=True)
    password = forms.CharField(widget=forms.PasswordInput)
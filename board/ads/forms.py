from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Reply


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['category', 'title', 'text']

       def clean(self):
           cleaned_data = super().clean()
           text = cleaned_data.get("text")
           if text is not None and len(text) < 20:
               raise ValidationError({
                   "description": "Текст не может быть меньше 20 символов."
               })

           return cleaned_data

class ReplyForm(forms.ModelForm):
    class Meta:
       model = Reply
       fields = ['text']

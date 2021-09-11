from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(label ='your name' ,max_length=264)
    sender = forms.EmailField(label='your email')
    receiver = forms.EmailField(label='reciver email')
    comments = forms.CharField(label='any comments?',
                                required = False,
                                widget=forms.Textarea)                       
            
    

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email','body')
    
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']


        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 5,
            }),
        }


        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'comment': 'Your Comment',
        }


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@example.com'):
            raise forms.ValidationError("Please use a valid email address from @example.com domain.")
        return email

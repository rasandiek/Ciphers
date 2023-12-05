from django import forms
from .models import Ciphers , Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label =" Profile Picture",required=False,)
    profile_bio = forms.CharField(label="Profile Bio",required=False, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Bio'}))
    homepage_link = forms.CharField(label="", required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website Link'}))
    facebook_link = forms.CharField(label="",required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Facebook Link'}))
    instagram_link = forms.CharField(label="", required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram Link'}))
    linkedin_link = forms.CharField(label="", required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Linkedin Link'}))

    class Meta:
        model = Profile
        fields =    ('profile_image' , 'profile_bio', 'homepage_link', 'facebook_link', 'instagram_link', 'linkedin_link', )

class CiphersForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           max_length=500,
                           widget=forms.widgets.Textarea(
                              attrs={
                                  "placeholder": "Post your Cipher....",
                                  "class": "form-control",
                                  "style": "background-color: #333333; color: white; border: 1px solid ##7117EA;"
                              }
                          ),
                          label="",
                          )


    class Meta:
        model = Ciphers
        exclude = ("user", "likes",)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address', 'style': 'color: #333333;'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name', 'style': 'color: #333333;'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name', 'style': 'color: #333333;'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['style'] = 'color: #333333;'
        self.fields['username'].help_text = '<span class="form-text text-muted" style="color: white !important;"><small >Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs['style'] = 'color: #333333;'
        self.fields['password1'].help_text = '<ul class="form-text text-muted small" style="color: white;"><li style="color: white;">Your password can\'t be too similar to your other personal information.</li><li style="color: white;">Your password must contain at least 8 characters.</li><li style="color: white;">Your password can\'t be a commonly used password.</li><li style="color: white;">Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].widget.attrs['style'] = 'color: #333333;'
        self.fields['password2'].help_text = '<span class="form-text text-muted" style="color: white;"><small style="color: white;">Enter the same password as before, for verification.</small></span>'

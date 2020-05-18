from django import forms
from working.models import Register


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({'class': 'form-control'}), label='Username', label_suffix="")
    password = forms.CharField(widget=forms.PasswordInput({'class': 'form-control'}), label='Password', label_suffix="")


class RegisterFrom(forms.Form, forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput({'class': 'form-control', 'placeholder': 'First Name'}),
                                 label="First Name", label_suffix="", min_length=1, max_length=100)
    last_name = forms.CharField(widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Last Name'}),
                                label="Last Name", label_suffix="", min_length=1, max_length=100)
    email = forms.CharField(widget=forms.EmailInput({'class': 'form-control', 'placeholder': 'example@mail.com'}),
                            label="Email", label_suffix="")
    password = forms.CharField(widget=forms.PasswordInput({'class': 'form-control'}), label='Password', label_suffix="")
    mobile = forms.CharField(widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Mobile'}),
                                 label="Mobile", label_suffix="", min_length=1, max_length=10)

    class Meta:
        model = Register
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'mobile',
        ]

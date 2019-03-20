from django.contrib.auth.forms import UsernameField, UserCreationForm
from django.contrib.auth.models import User
from cvat.apps.engine.models import Label
from django.utils.translation import gettext, gettext_lazy as _
from django import forms


class CustomUserForm(UserCreationForm):
    username = UsernameField(
        label=_("UserID"),
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': "UserID"}),
        required=True,
    )

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'placeholder': "Email"}),
        required=True,
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': "Password"}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'placeholder': "Password confirmation"}),
        strip=False,
    )
    
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


prefix_choice = [
    (1, 'Unique'),
    (2, 'Temporary'),
]

input_choice = [
    (1, 'Select'),
    (2, 'Checkbox'),
    (3, 'Radio'),
    (4, 'Number'),
    (5, 'Text'),
]

class LabelForm(forms.Form):
    label = forms.CharField(max_length=64,label='Label')
    attribute = forms.CharField(max_length=64, label='Attribute')
    prefix = forms.ChoiceField(choices=prefix_choice, initial=1, label='Prefix')
    input_type = forms.ChoiceField(choices=input_choice, initial=1, label='Input Type')
    value1 = forms.CharField(max_length=64, label='Attribute Value1')
    value2 = forms.CharField(max_length=64, label='Attribute Value2')
    value3 = forms.CharField(max_length=64, label='Attribute Value3')

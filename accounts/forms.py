from django import forms
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import datetime

from accounts.models import Token


class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']


class VerifyEmailForm(forms.Form):
    token = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)

    def clean(self):
        token_name = self.data['token']
        email = self.data['email']

        token = Token.objects.filter(name=token_name, expiry_date__gte=datetime.utcnow(),
                                     user__email=email, user__verified_email=False).first()
        if not token:
            raise forms.ValidationError('expired token value')

        return super().clean()

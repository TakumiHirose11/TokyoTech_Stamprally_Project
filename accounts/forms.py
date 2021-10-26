from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.forms import fields
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)

UserModel = get_user_model()

#ログイン用フォーム
class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label=_("Password"), strip=False,
                               widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': "Eメールアドレス または パスワードに誤りがあります。",
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the label for the "email" field.
        self.email_field = UserModel._meta.get_field("email")
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.email_field.verbose_name)
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        email_len=len(email)
        m_address=email[email_len-14:]

        #mアドレス認証
        if not m_address=="m.titech.ac.jp":
            raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': self.email_field.verbose_name})

        


        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': self.email_field.verbose_name})
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'], code='inactive')
    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None
    def get_user(self):
        return self.user_cache

#ログイン用フォームver.2


User = get_user_model()


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()

        #mアドレス認証
        email_len=len(email)
        m_address=email[email_len-14:]
        if not m_address=="m.titech.ac.jp":
            raise forms.ValidationError('mアドレスを使ってください！')
        
        return email

from accounts.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        SELECTION1=(('a','学院はどこですか？'),('b','部活・サークルは？'),('c','出身県はどこですか？'),('d','出身高校はどこですか？'),('e','興味のある分野はなんですか？'),('f','将来の夢はなんですか？'))
        fields=('unit','profile_picture','nickname','comment','question1','question2','answer1','answer2',)
from django import forms


class LoginCredentialForm(forms.Form):

    username = forms.CharField(label="Имя")
    password = forms.CharField(label="Пароль")
    email = forms.CharField(label="Почта")

    class Meta:
        fields = [
            'username',
            'password',
            'email'
        ]


class LoginKeyForm(forms.Form):

    key = forms.CharField(label="Введите код")

    class Meta:
        fields = [
            'key',
        ]
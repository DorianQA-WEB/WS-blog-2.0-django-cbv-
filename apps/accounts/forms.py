from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile


class UserUpdateForm(forms.ModelForm):
        """
        Форма обновления данных пользователя
        """
        username = forms.CharField(max_length=100,
                                   widget=forms.TextInput(attrs={'class': 'form-control mb-1'}))
        email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb-1'}))
        first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-1'}))
        last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-1'}))


        class Meta:
            model = User
            fields = ('username', 'email', 'first_name', 'last_name')


        def clean_email(self):
            """
            Проверка email на уникальность
            """
            email = self.cleaned_data.get('email')
            if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Этот email уже используется')
            return email


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма обновления данных профиля пользователя
    """
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-1'})
    )
    bio = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control mb-1'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control mb-1'}))

    class Meta:
        model = Profile
        fields = ('birth_date', 'bio', 'avatar')


class UserRegisterForm(UserCreationForm):
    """
    Переопределенная форма регистрации пользователей
    """

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется')
        return email

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы регистрации
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': "Придумайте свой логин"})
        self.fields['password1'].widget.attrs.update({'placeholder': "Придумайте пароль"})
        self.fields['password2'].widget.attrs.update({'placeholder': "Повторите пароль"})
        self.fields['email'].widget.attrs.update({'placeholder': "Введите ваш email"})
        self.fields['first_name'].widget.attrs.update({'placeholder': "Введите ваше имя"})
        self.fields['last_name'].widget.attrs.update({'placeholder': "Введите вашу фамилию"})
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})


class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации на сайте
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы авторизации
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
        self.fields['username'].label = 'Логин'
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control',
                                                    'autocomplete': 'off'})
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .model_backup import Product, Category

# Use get_user_model() to avoid potential import conflicts
User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Username kiriting'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email kiriting'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ismingizni kiriting'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Familiyangizni kiriting'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Parol kiriting'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Parolni takrorlang'})


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'stock', 'featured']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mahsulot nomini kiriting'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Mahsulot tavsifini kiriting'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01', 'placeholder': '0.00'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Parol',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yangi parol (ixtiyoriy)'
        }),
        required=False
    )
    password2 = forms.CharField(
        label='Parolni tasdiqlash',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni takrorlang'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username kiriting'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email kiriting'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ism kiriting'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Familiya kiriting'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Parollar mos kelmaydi!")
            if len(password1) < 8:
                raise forms.ValidationError("Parol kamida 8 ta belgidan iborat bo'lishi kerak!")

        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kategoriya nomini kiriting'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Kategoriya tavsifini kiriting'
            })
        }
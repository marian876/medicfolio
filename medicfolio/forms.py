from django import forms
from users.models import User, Profile

class RegisterForm(forms.Form):
    
    username= forms.CharField(label='Usuario',
                              required=True, 
                              min_length=4, max_length=50, 
                              widget=forms.TextInput(attrs={
                                  'class':'form-control',
                                  'id': 'username',
                                  'placeholder':'Ingrese su nombre de usuario'
                              }))
    first_name = forms.CharField(label='Nombre',
                                required=True, 
                                min_length=2, max_length=50,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Ingrese su nombre'
                              }))
    last_name = forms.CharField(
                                label='Apellido',
                                required=True, 
                                min_length=2, max_length=50,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Ingrese su apellido'
                                }))
    email=forms.EmailField(required=True, 
                              min_length=4, max_length=50, 
                              widget=forms.EmailInput(attrs={
                                  'class':'form-control',
                                  'id': 'emal',
                                  'placeholder':'Ingrese su correo electónico'
                              }))
    password=forms.CharField(label='Contraseña',
                              required=True, 
                              min_length=4, max_length=50, 
                              widget=forms.PasswordInput(attrs={
                                  'class':'form-control',
                                  'id': 'password',
                                  'placeholder':'Ingrese su contraseña'
                              }))
    password2=forms.CharField(label='Confirmar contraseña',
                              required=True, 
                              min_length=4, max_length=50, 
                              widget=forms.PasswordInput(attrs={
                                  'class':'form-control',
                                  'id': 'password',
                                  'placeholder':'Ingrese su contraseña'
                              }))
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    encargado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    alergias = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    enfermedades_base = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    cirugias = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    enfermedades_familiares = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    historial = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    foto = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    def clean_username(self):
        username=self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')
        
        return username
    
    def clean_email(self):
        email=self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo ya se encuentra en uso')
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2','La contraseña no coincide')
    
    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)

        if commit:
            user.save()

        profile = user.profile if hasattr(user, 'profile') else Profile(user=user)

        if self.cleaned_data.get('foto'):
            profile.foto = self.cleaned_data['foto']

        profile.historial = self.cleaned_data.get('historial', profile.historial)
        profile.fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento', profile.fecha_nacimiento)
        profile.encargado = self.cleaned_data.get('encargado', profile.encargado)
        profile.alergias = self.cleaned_data.get('alergias', profile.alergias)
        profile.enfermedades_base = self.cleaned_data.get('enfermedades_base', profile.enfermedades_base)
        profile.cirugias = self.cleaned_data.get('cirugias', profile.cirugias)
        profile.enfermedades_familiares = self.cleaned_data.get('enfermedades_familiares', profile.enfermedades_familiares)

        if commit:
            profile.save()

        return user
        
class UserEditForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    encargado = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    alergias = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    enfermedades_base = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    cirugias = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    enfermedades_familiares = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    historial = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False
    )
    foto = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        # Si el formulario tiene una instancia, entonces estamos editando un usuario existente
        if self.instance and hasattr(self.instance, 'profile'):
            # Inicializa los campos del formulario con los valores del perfil
            self.fields['fecha_nacimiento'].initial = self.instance.profile.fecha_nacimiento
            self.fields['encargado'].initial = self.instance.profile.encargado
            self.fields['alergias'].initial = self.instance.profile.alergias
            self.fields['enfermedades_base'].initial = self.instance.profile.enfermedades_base
            self.fields['cirugias'].initial = self.instance.profile.cirugias
            self.fields['enfermedades_familiares'].initial = self.instance.profile.enfermedades_familiares
            self.fields['historial'].initial = self.instance.profile.historial
            self.fields['foto'].initial = self.instance.profile.foto

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)

        if commit:
            user.save()

        profile = user.profile if hasattr(user, 'profile') else Profile(user=user)

        if self.cleaned_data.get('foto'):
            profile.foto = self.cleaned_data['foto']
            profile.save()

        return user

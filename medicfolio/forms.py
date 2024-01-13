from django import forms
from users.models import User, Profile


class RegisterForm(forms.Form):
    
    username= forms.CharField(label='Nombre de usuario',
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
    
    def save(self):
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
        )
        profile = Profile.objects.create(
            user=user,
            fecha_nacimiento=self.cleaned_data.get('fecha_nacimiento'),
            encargado=self.cleaned_data.get('encargado', ''),
            alergias=self.cleaned_data.get('alergias', 'No especificado'),
            enfermedades_base=self.cleaned_data.get('enfermedades_base', ''),
            cirugias=self.cleaned_data.get('cirugias', ''),
            enfermedades_familiares=self.cleaned_data.get('enfermedades_familiares', ''),
            foto=self.cleaned_data.get('foto')
        )

        return user
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import PatientProfile, CareProfile, FamilyProfile,User, Doctor
from django.contrib.auth import get_user_model
from django.forms import DateInput
from django.contrib.auth.hashers import make_password


User = get_user_model()

class UserEditForm(forms.ModelForm):
    # Campos adicionales del modelo User
    first_name = forms.CharField(max_length=30, required=False, label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label='Correo electrónico', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    # Campos específicos del modelo PatientProfile
    celular = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    medico = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        required=False,
        label='Médico tratante',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    seguro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Seguro médico - N° contrato', required=False)
    fecha_nacimiento = forms.DateField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    alergias = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), 
        required=False
    )
    enfermedades_base = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), 
        required=False
    )
    cirugias = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), 
        required=False
    )
    enfermedades_familiares = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), 
        required=False
    )
    historial = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    foto = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}), required=False)
    encargado = forms.ModelChoiceField(queryset=User.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        self.profile_instance = kwargs.pop('profile_instance', None)
        super(UserEditForm, self).__init__(*args, **kwargs)

        if self.profile_instance:
            profile = self.profile_instance
            self.fields['celular'].initial = profile.celular
            self.fields['seguro'].initial = profile.seguro
            self.fields['medico'].initial = self.profile_instance.medico
            self.fields['alergias'].initial = profile.alergias
            self.fields['enfermedades_base'].initial = profile.enfermedades_base
            self.fields['cirugias'].initial = profile.cirugias
            self.fields['enfermedades_familiares'].initial = profile.enfermedades_familiares
            self.fields['historial'].initial = profile.historial
            self.fields['encargado'].initial = profile.encargado
            self.fields['foto'].initial = profile.foto
            if profile.fecha_nacimiento:
                self.fields['fecha_nacimiento'].initial = profile.fecha_nacimiento.strftime("%Y-%m-%d")

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        if commit:
            user.save()

        if not hasattr(user, 'patientprofile'):
            user.patientprofile = PatientProfile(user=user)

        profile = user.patientprofile
        profile.celular = self.cleaned_data.get('celular')
        profile.seguro = self.cleaned_data.get('seguro')
        profile.medico = self.cleaned_data.get('medico')
        profile.fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        profile.alergias = self.cleaned_data.get('alergias')
        profile.enfermedades_base = self.cleaned_data.get('enfermedades_base')
        profile.cirugias = self.cleaned_data.get('cirugias')
        profile.enfermedades_familiares = self.cleaned_data.get('enfermedades_familiares')
        profile.historial = self.cleaned_data.get('historial')
        profile.encargado = self.cleaned_data.get('encargado')
        if 'foto' in self.cleaned_data and self.cleaned_data['foto'] is not None:
            profile.foto = self.cleaned_data['foto']

        if commit:
            profile.save()

        return user

class SignUpForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.exclude(name='Administrador'), required=True)

    class Meta:
        model = User  
        fields = ['username', 'first_name', 'last_name', 'email', 
                  'password', 'password2', 'group']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['group'].widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Un usuario con ese nombre de usuario ya existe.")
        return username

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

    group = forms.ModelChoiceField(
        queryset=Group.objects.exclude(name='Administrador'),
        label='Grupo',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'group']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo electrónico ya está en uso')
        return email

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['password'])  # Encriptar la contraseña correctamente
        if commit:
            user.save()
            user.groups.add(self.cleaned_data['group'])  # Asignar grupo
        return user

    
class FamilyProfileForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Paciente'),
        required=False,
        label='Paciente',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    parentezco = forms.CharField(
        max_length=100, 
        required=False, 
        label='Parentezco', 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    celular = forms.CharField(
        max_length=15, 
        required=False, 
        label='Teléfono', 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cohabitacion = forms.BooleanField(
        required=False, 
        label='Cohabitación con el paciente', 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = FamilyProfile
        fields = ['paciente', 'parentezco', 'celular', 'cohabitacion']

    def __init__(self, *args, **kwargs):
        super(FamilyProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        family_profile = super(FamilyProfileForm, self).save(commit=False)
        if commit:
            family_profile.save()
        return family_profile

class CareProfileForm(forms.ModelForm):
    celular = forms.CharField(
        max_length=15, 
        required=False, 
        label='Teléfono', 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    experiencia = forms.CharField(
        required=False, 
        label='Experiencia laboral', 
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    habilidades = forms.CharField(
        required=False, 
        label='Habilidades', 
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    educacion = forms.CharField(
        required=False, 
        label='Educación', 
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    recomendacion = forms.CharField(
        required=False, 
        label='Recomendaciones', 
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    disponibilidad = forms.CharField(
        required=False, 
        label='Disponibilidad', 
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    comentario = forms.CharField(
        required=False, 
        label='Comentarios adicionales', 
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    foto = forms.ImageField(
        required=False,
        label='Foto',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CareProfile
        fields = ['celular', 'experiencia', 'habilidades', 'educacion', 'recomendacion', 'disponibilidad', 'comentario', 'foto']

    def __init__(self, *args, **kwargs):
        self.profile_instance = kwargs.pop('profile_instance', None)
        super(CareProfileForm, self).__init__(*args, **kwargs)
        
        if self.profile_instance:
            profile = self.profile_instance
            self.fields['celular'].initial = profile.celular
            self.fields['experiencia'].initial = profile.experiencia
            self.fields['habilidades'].initial = profile.habilidades
            self.fields['educacion'].initial = profile.educacion
            self.fields['recomendacion'].initial = profile.recomendacion
            self.fields['disponibilidad'].initial = profile.disponibilidad
            self.fields['comentario'].initial = profile.comentario
            self.fields['foto'].initial = profile.foto

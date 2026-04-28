from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ContactMessage, CommunityWaitlist, MemberProfile, ForumTopic, ForumReply, ForumCategory, ForumReport

_INPUT_CLASS = (
    'w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 '
    'focus:outline-none focus:border-yellow-400 transition-colors placeholder-gray-500'
)

_TEXTAREA_CLASS = (
    'w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 '
    'focus:outline-none focus:border-yellow-400 transition-colors resize-none placeholder-gray-500'
)

_SELECT_CLASS = (
    'w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 '
    'focus:outline-none focus:border-yellow-400 transition-colors appearance-none cursor-pointer'
)

_CHECKBOX_CLASS = 'w-4 h-4 rounded border-gray-600 bg-gray-800 text-yellow-400 focus:ring-yellow-400'


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'interest', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Numele tău',
                'class': _INPUT_CLASS,
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Numărul tău de telefon (opțional)',
                'class': _INPUT_CLASS,
            }),
            'interest': forms.Select(attrs={
                'class': _SELECT_CLASS,
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Mesajul tău...',
                'rows': 5,
                'class': _TEXTAREA_CLASS,
            }),
        }
        labels = {
            'name': 'Nume',
            'phone': 'Telefon',
            'interest': 'Ce te interesează?',
            'message': 'Mesaj',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['interest'].required = False
        self.fields['interest'].choices = [
            ('', '— Ce te interesează? —'),
            ('catalog', 'Catalog / Modele'),
            ('comunitate', 'Comunitate / Forum'),
            ('evenimente', 'Evenimente / Tururi'),
            ('altele', 'Altele'),
        ]



class CommunityWaitlistForm(forms.ModelForm):
    class Meta:
        model = CommunityWaitlist
        fields = ['name', 'email', 'city', 'owns_jetski', 'favorite_brand', 'message', 'wants_updates']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Numele tău complet',
                'class': _INPUT_CLASS,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'adresa@email.ro',
                'class': _INPUT_CLASS,
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Orașul tău (opțional)',
                'class': _INPUT_CLASS,
            }),
            'owns_jetski': forms.CheckboxInput(attrs={
                'class': _CHECKBOX_CLASS,
            }),
            'favorite_brand': forms.Select(attrs={
                'class': _SELECT_CLASS,
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'De ce vrei să faci parte din comunitate? (opțional)',
                'rows': 3,
                'class': _TEXTAREA_CLASS,
            }),
            'wants_updates': forms.CheckboxInput(attrs={
                'class': _CHECKBOX_CLASS,
            }),
        }
        labels = {
            'name': 'Nume',
            'email': 'Email',
            'city': 'Oraș',
            'owns_jetski': 'Am deja un jet-ski',
            'favorite_brand': 'Brand preferat',
            'message': 'Mesaj (opțional)',
            'wants_updates': 'Vreau să primesc noutăți despre lansare și evenimente',
        }


_BRAND_CHOICES = [
    ('', '— Alege brand —'),
    ('sea-doo', 'Sea-Doo'),
    ('yamaha', 'Yamaha'),
    ('kawasaki', 'Kawasaki'),
    ('other', 'Alt brand'),
    ('none', 'Nu am încă'),
]


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        label='Nume complet',
        widget=forms.TextInput(attrs={'placeholder': 'Prenume și nume', 'class': _INPUT_CLASS}),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'adresa@email.ro', 'class': _INPUT_CLASS, 'autocomplete': 'email'}),
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        label='Oraș',
        widget=forms.TextInput(attrs={'placeholder': 'Orașul tău (opțional)', 'class': _INPUT_CLASS}),
    )
    owns_jetski = forms.BooleanField(
        required=False,
        label='Am deja un jet-ski',
        widget=forms.CheckboxInput(attrs={'class': 'w-4 h-4 rounded border-gray-600 bg-gray-800 text-yellow-400 focus:ring-yellow-400'}),
    )
    favorite_brand = forms.ChoiceField(
        choices=_BRAND_CHOICES,
        required=False,
        label='Brand preferat',
        widget=forms.Select(attrs={'class': (
            'w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 '
            'focus:outline-none focus:border-yellow-400 transition-colors appearance-none cursor-pointer'
        )}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': 'Alege o parolă', 'class': _INPUT_CLASS})
        self.fields['password1'].label = 'Parolă'
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repetă parola', 'class': _INPUT_CLASS})
        self.fields['password2'].label = 'Confirmă parola'

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Există deja un cont cu această adresă de email.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data['first_name']
        user.email = email
        user.username = email[:150]
        if commit:
            user.save()
            profile = user.profile
            profile.city = self.cleaned_data.get('city', '')
            profile.owns_jetski = self.cleaned_data.get('owns_jetski', False)
            profile.favorite_brand = self.cleaned_data.get('favorite_brand', '')
            profile.save()
        return user


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        label='Nume complet',
        widget=forms.TextInput(attrs={'placeholder': 'Prenume și nume', 'class': _INPUT_CLASS}),
    )

    class Meta:
        model = MemberProfile
        fields = ['city', 'owns_jetski', 'favorite_brand', 'bio', 'avatar', 'show_in_directory']
        widgets = {
            'city': forms.TextInput(attrs={'placeholder': 'Orașul tău', 'class': _INPUT_CLASS}),
            'owns_jetski': forms.CheckboxInput(attrs={'class': 'w-4 h-4 rounded border-gray-600 bg-gray-800 text-yellow-400 focus:ring-yellow-400'}),
            'favorite_brand': forms.Select(
                choices=_BRAND_CHOICES,
                attrs={'class': (
                    'w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 '
                    'focus:outline-none focus:border-yellow-400 transition-colors appearance-none cursor-pointer'
                )},
            ),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Câteva cuvinte despre tine și pasiunea ta pentru jet-ski...',
                'rows': 4,
                'class': (
                    'w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 '
                    'focus:outline-none focus:border-yellow-400 transition-colors resize-none placeholder-gray-500'
                ),
            }),
            'avatar': forms.ClearableFileInput(attrs={'class': 'hidden', 'id': 'avatar-upload', 'accept': 'image/*'}),
            'show_in_directory': forms.CheckboxInput(attrs={'class': 'w-4 h-4 rounded border-gray-600 bg-gray-800 text-cyan-400 focus:ring-cyan-400'}),
        }
        labels = {
            'city': 'Oraș',
            'owns_jetski': 'Am deja un jet-ski',
            'favorite_brand': 'Brand preferat',
            'bio': 'Despre mine',
            'avatar': 'Avatar',
            'show_in_directory': 'Arată profilul meu în lista membrilor',
        }


class EmailLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs.update({
            'placeholder': 'adresa@email.ro',
            'class': _INPUT_CLASS,
            'autocomplete': 'email',
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Parola ta',
            'class': _INPUT_CLASS,
            'autocomplete': 'current-password',
        })
        self.fields['password'].label = 'Parolă'


class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['category', 'title', 'content']
        widgets = {
            'category': forms.Select(attrs={'class': (
                'w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 '
                'focus:outline-none focus:border-yellow-400 transition-colors appearance-none cursor-pointer'
            )}),
            'title': forms.TextInput(attrs={
                'placeholder': 'Titlul subiectului tău...',
                'class': _INPUT_CLASS,
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Descrie subiectul în detaliu...',
                'rows': 10,
                'class': (
                    'w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 '
                    'focus:outline-none focus:border-yellow-400 transition-colors resize-y placeholder-gray-500'
                ),
            }),
        }
        labels = {
            'category': 'Categorie',
            'title': 'Titlu',
            'content': 'Conținut',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ForumCategory.objects.filter(is_active=True)
        self.fields['category'].empty_label = '— Alege o categorie —'


class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Scrie răspunsul tău...',
                'rows': 5,
                'class': (
                    'w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 '
                    'focus:outline-none focus:border-yellow-400 transition-colors resize-y placeholder-gray-500'
                ),
            }),
        }
        labels = {'content': 'Răspuns'}


class ForumReportForm(forms.ModelForm):
    class Meta:
        model = ForumReport
        fields = ['reason', 'details']
        widgets = {
            'reason': forms.Select(attrs={'class': (
                'w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 '
                'focus:outline-none focus:border-yellow-400 transition-colors appearance-none cursor-pointer'
            )}),
            'details': forms.Textarea(attrs={
                'placeholder': 'Descrie pe scurt problema (opțional)...',
                'rows': 4,
                'class': (
                    'w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 '
                    'focus:outline-none focus:border-yellow-400 transition-colors resize-none placeholder-gray-500'
                ),
            }),
        }
        labels = {
            'reason': 'Motiv raportare',
            'details': 'Detalii suplimentare (opțional)',
        }

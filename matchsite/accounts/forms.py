from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

GENDER_FORM_CHOICES = [("M", "Male"), ("F", "Female")]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """A FileField whose widget lets the user pick several files at once."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)


class BootstrapFormMixin:
    """Adds the 'form-control' class to every widget so plain {{ field }} looks decent."""

    def _style_fields(self):
        for name, field in self.fields.items():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " " + css).strip()


class RegistrationForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=True
    )
    gender = forms.ChoiceField(choices=GENDER_FORM_CHOICES)
    looking_for = forms.ChoiceField(choices=GENDER_FORM_CHOICES, label="Interested in")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_birth_date(self):
        from datetime import date

        birth_date = self.cleaned_data["birth_date"]
        age = date.today().year - birth_date.year - (
            (date.today().month, date.today().day) < (birth_date.month, birth_date.day)
        )
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        return birth_date


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    extra_photos = MultipleFileField(
        required=False,
        label="Add more photos",
        help_text="You can select several images at once.",
    )

    class Meta:
        model = Profile
        fields = ["birth_date", "gender", "looking_for", "city", "country", "bio", "photo"]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {"looking_for": "Interested in", "photo": "Main / cover photo"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()
        self.fields["extra_photos"].widget.attrs["class"] = "form-control"
        self.fields["extra_photos"].widget.attrs["multiple"] = True

    def clean_birth_date(self):
        from datetime import date

        birth_date = self.cleaned_data["birth_date"]
        if birth_date:
            age = date.today().year - birth_date.year - (
                (date.today().month, date.today().day) < (birth_date.month, birth_date.day)
            )
            if age < 18:
                raise forms.ValidationError("You must be at least 18 years old to use Waslni.")
        return birth_date

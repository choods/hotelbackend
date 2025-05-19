# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class CustomUserChangeForm(forms.ModelForm):
    phone_number = forms.CharField(label='Phone Number', required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the current phone number from the Profile model
        if self.instance.pk:
            try:
                self.fields['phone_number'].initial = self.instance.profile.phone_number
            except Profile.DoesNotExist:
                self.fields['phone_number'].initial = ""

    def save(self, commit=True):
        user = super().save(commit)
        phone = self.cleaned_data.get('phone_number', '')

        # Save phone number to the Profile model
        Profile.objects.update_or_create(user=user, defaults={'phone_number': phone})
        return user

from django import forms

from .models import ContactInquiry


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'subject',
            'service',
            'message',
            'terms',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'firstName', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'id': 'lastName', 'placeholder': 'Doe'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'placeholder': 'john@example.com'}),
            'phone': forms.TextInput(attrs={'id': 'phone', 'placeholder': '+1 234 567 890'}),
            'subject': forms.TextInput(attrs={'id': 'subject', 'placeholder': 'How can we help you?'}),
            'service': forms.Select(attrs={'id': 'service', 'class': 'form-select'}),
            'message': forms.Textarea(attrs={'id': 'message', 'rows': 5, 'placeholder': 'Describe your legal matter...'}),
            'terms': forms.CheckboxInput(attrs={'id': 'terms'}),
        }

    def clean_terms(self):
        accepted = self.cleaned_data.get('terms')
        if not accepted:
            raise forms.ValidationError('Please accept the terms and privacy policy.')
        return accepted

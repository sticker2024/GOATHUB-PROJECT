from django import forms
from .models import FarmerRegistration, VetConsultation, SpecialCase, Veterinary  # Import Veterinary model

class FarmerRegistrationForm(forms.ModelForm):
    class Meta:
        model = FarmerRegistration
        fields = ['first_name', 'last_name', 'id_number', 'phone_number', 'district', 'password']


class VetConsultationForm(forms.ModelForm):
    class Meta:
        model = VetConsultation
        fields = ['full_name', 'phone_number', 'location', 'message', 'image']


class SpecialCaseForm(forms.ModelForm):
    class Meta:
        model = SpecialCase
        fields = ['image', 'district', 'sector', 'description']
        labels = {
            'image': 'Upload Image',
            'district': 'District',
            'sector': 'Sector',
            'description': 'Description of the Case',
        }
        help_texts = {
            'description': 'Please provide a detailed description of the special case.',
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validate the file type
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("Image must be a PNG, JPG, or JPEG file.")
            # Validate the file size (e.g., max 5MB)
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image size must not exceed 5 MB.")
        return image


class VeterinaryForm(forms.ModelForm):
    class Meta:
        model = Veterinary
        fields = ['name', 'email', 'phone', 'district', 'specialty']
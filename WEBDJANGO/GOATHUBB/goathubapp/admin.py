from django.contrib import admin
from .models import FarmerRegistration, VetConsultation, Veterinary, SpecialCase, ConsultationReply

class FarmerRegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'id_number', 'phone_number', 'district')  # Columns to display
    search_fields = ('first_name', 'last_name', 'id_number', 'phone_number')  # Searchable fields
    list_filter = ('district',)  # Filter by district

class VetConsultationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'location', 'created_at')  # Columns to display
    search_fields = ('full_name', 'phone_number', 'location', 'message')  # Searchable fields
    list_filter = ('created_at',)  # Filter by creation date

class VeterinaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'district', 'specialty')  # Columns to display
    search_fields = ('name', 'email', 'phone')  # Searchable fields
    list_filter = ('district', 'specialty')  # Filter by district and specialty

class SpecialCaseAdmin(admin.ModelAdmin):
    list_display = ('district', 'sector', 'description')  # Columns to display
    search_fields = ('district', 'sector')  # Searchable fields

class ConsultationReplyAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'reply_message', 'created_at')  # Columns to display
    search_fields = ('consultation__full_name', 'reply_message')  # Searchable fields
    list_filter = ('created_at',)  # Filter by creation date

# Register the models with the admin site
admin.site.register(FarmerRegistration, FarmerRegistrationAdmin)
admin.site.register(VetConsultation, VetConsultationAdmin)
admin.site.register(Veterinary, VeterinaryAdmin)
admin.site.register(SpecialCase, SpecialCaseAdmin)
admin.site.register(ConsultationReply, ConsultationReplyAdmin)
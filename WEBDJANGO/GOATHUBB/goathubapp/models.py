from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class FarmerRegistration(models.Model):
    registration_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=50, unique=True)  # Unique ID number for each farmer
    phone_number = models.CharField(max_length=15)
    district = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password and not self.password.startswith('pbkdf2:'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Compare hashed password

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id_number})"

class VetConsultation(models.Model):
    consultation_id = models.AutoField(primary_key=True)  # Custom consultation ID
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    message = models.TextField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)  # Optional image field
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the consultation was created

    def __str__(self):
        return f"Consultation Request from {self.full_name} (ID: {self.consultation_id})"

class Veterinary(models.Model):
    veterinary_id = models.AutoField(primary_key=True)  # Custom veterinary ID
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Unique email address
    phone = models.CharField(max_length=15)
    district = models.CharField(max_length=100)
    specialty = models.CharField(max_length=50)  # Store specialty as a string

    def __str__(self):
        return f"{self.name} - {self.specialty}"

class SpecialCase(models.Model):
    case_id = models.AutoField(primary_key=True)  # Custom case ID
    image = models.ImageField(upload_to='special_cases/')  # Field for the uploaded image
    district = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Special Case in {self.district} - {self.sector}"

class ConsultationReply(models.Model):
    reply_id = models.AutoField(primary_key=True)  # Custom reply ID
    consultation = models.ForeignKey(VetConsultation, on_delete=models.CASCADE, related_name='replies')  # Link to the consultation
    reply_message = models.TextField()  # Message from the veterinary
    reply_image = models.ImageField(upload_to='replies/', blank=True, null=True)  # Optional image for the reply
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the reply was created
    farmer_name = models.CharField(max_length=100, null=True)  # Field for the sender's full name (allow null)

    def __str__(self):
        return f"Reply from {self.farmer_name} to Consultation ID: {self.consultation.consultation_id} - Reply ID: {self.reply_id}"
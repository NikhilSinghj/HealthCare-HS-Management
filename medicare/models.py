from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=40)
    blood_group = models.CharField(max_length=40,null=True)

    

class Dropdown(models.Model):
    departments = models.CharField(max_length=100,null=True,unique=True)
    deleted_status=models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Dropdown'


class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True)
    department=models.ForeignKey(Dropdown,on_delete=models.DO_NOTHING,null=True)
    qualification = models.CharField(max_length=50)
    doctorFee=models.PositiveIntegerField(null=False)
    deleted_status=models.BooleanField(default=False)

    class Meta:
        db_table = 'Doctors_details' 




class Appointment(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    department=models.ForeignKey(Dropdown,on_delete=models.DO_NOTHING,null=True)
    doctor_id=models.PositiveIntegerField(null=True)
    appointmentDate=models.DateField(null=True)
    approvedby_doctor = models.BooleanField(default=False)
    approvedby_receptionist = models.BooleanField(default=False)
    checkup_status = models.BooleanField(default=False)
    checkup_date = models.DateField(null=True)
    time=models.CharField(max_length=20,null=True)
    payment_status=models.BooleanField(default=False)
    deleted_status=models.BooleanField(default=False)

    class Meta:
        db_table = 'Appointment_details' 


class Patient(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    doctor=models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,null=True)
    admitDate = models.DateField(auto_now=True)
    releaseDate = models.DateField(null=False)
    symptoms = models.CharField(max_length=100,null=True)
    prescriptions = models.CharField(max_length=100,null=True)
    deleted_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'Patients_details' 
    





class PaymentDetails(models.Model):
    user=models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True)
    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)

    class Meta:
        db_table = 'Payment_details' 
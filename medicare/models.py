from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=40)
    

    

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
    doctor_name=models.CharField(max_length=50,null=True)
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


class Medicalhistory(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    blood_group = models.CharField(max_length=40,null=True)
    height = models.PositiveIntegerField(null=True)
    weight = models.PositiveIntegerField(null=True)
    alcoholic=models.BooleanField(default=False)
    smoker=models.BooleanField(default=False)
    symptoms = models.CharField(max_length=100,null=True)
    deleted_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'Medical_history' 
    





class Prescription(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    medicine=models.CharField(max_length=50,null=True)
    quantity=models.PositiveIntegerField(null=True)
    price=models.PositiveIntegerField(null=True)
    prescription_date=models.DateField(auto_now=True)
    deleted_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'Prescriptinons_details' 


class Instructuns(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    instructions=models.TextField(max_length=50,null=True)
    deleted_status = models.BooleanField(default=False)

    class Meta:
        db_table= 'Instructions'


class Leftpanel(models.Model):
    panel=models.CharField(max_length=50,null=False)
    dashboard=models.CharField(max_length=30,null=False)
    deleted_status = models.BooleanField(default=False)

    class Meta:
        db_table='Leftpannel'
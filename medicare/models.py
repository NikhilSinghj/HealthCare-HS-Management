from django.db import models

from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(max_length=50)
    


class User(AbstractUser):
    first_name=None
    last_name=None
    roles = models.ManyToManyField(Role)
    
    
    

class Dropdown(models.Model):
    departments = models.CharField(max_length=100,null=True,unique=True)
    deleted_status=models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Dropdown'


class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=100)

    class Meta:
        db_table= 'patient_detail'



class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True)
    department=models.ForeignKey(Dropdown,on_delete=models.DO_NOTHING,null=True)
    first_name=models.CharField(max_length=50,null=True)
    last_name=models.CharField(max_length=50,null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10,null=True)
    contact = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=100,null=True)
    qualification = models.CharField(max_length=50)
    doctorFee=models.PositiveIntegerField(null=False)
    deleted_status=models.BooleanField(default=False)

    class Meta:
        db_table = 'doctors_details' 




class Appointment(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.DO_NOTHING,null=True)
    department=models.ForeignKey(Dropdown,on_delete=models.DO_NOTHING,null=True)
    doctor=models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,null=True)
    appointmentDate=models.DateField(null=True)
    approvedby_doctor = models.BooleanField(default=False)
    approvedby_receptionist = models.BooleanField(default=False)
    checkup_status = models.CharField(max_length=20,default='Not Checked')
    checkup_date = models.DateField(null=True)
    time=models.CharField(max_length=50,null=True)
    symptoms = models.CharField(max_length=100,null=True)
    payment_status=models.CharField(max_length=20,default='Pending')
    deleted_status=models.BooleanField(default=False)

    class Meta:
        db_table = 'Appointment_details' 


class Medicalhistory(models.Model):
    patient=models.OneToOneField(Patient,on_delete=models.DO_NOTHING,null=True)
    blood_group = models.CharField(max_length=40,null=True)
    height = models.PositiveIntegerField(null=True)
    weight = models.PositiveIntegerField(null=True)
    alcoholic=models.CharField(max_length=20,default='No')
    smoker=models.CharField(max_length=20,default='No')
    deleted_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'Medical_history' 
    





class Prescription(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.DO_NOTHING,null=True)
    doctor=models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,null=True)
    medicine=models.CharField(max_length=50,null=True)
    quantity=models.PositiveIntegerField(null=True)
    dosage=models.CharField(max_length=50,null=True)
    timing=models.CharField(max_length=50,null=True)
    prescription_date=models.DateField(auto_now=True)
    deleted_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'Prescriptinons_details' 


class Instructuns(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.DO_NOTHING,null=True)
    instructions=models.TextField(max_length=50,null=True)
    deleted_status = models.BooleanField(default=False)

    class Meta:
        db_table= 'Instructions'


class Leftpanel(models.Model):
    role=models.ForeignKey(Role,on_delete=models.DO_NOTHING,null=True)
    panel=models.CharField(max_length=50,null=False)
    state=models.TextField(max_length=50,blank=True)
    icons=models.TextField(max_length=50,null=True)
    order=models.IntegerField(default='0')
    deleted_status = models.BooleanField(default=False)

    class Meta:
        db_table='Leftpanel'


class Slots(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,null=True)
    slots = models.CharField(max_length=50,null=True)
    deleted_status=models.BooleanField(default=False)
    
    class Meta:
        db_table = 'avialable_slots'


class Tests(models.Model):
    test = models.CharField(max_length=100,null=True,unique=True)
    deleted_status=models.BooleanField(default=False)
    
    class Meta:
        db_table = 'avialable_tests'
from django.shortcuts import render

from django.http import JsonResponse,HttpResponse
import json
import re
from .models import User,Doctor,Appointment,Dropdown,Leftpanel,Medicalhistory,Role
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.template.loader import render_to_string



# ----------------------------------------------------- Registration and login/logout -----------------------------------------------

def register_doctor(request):
    if request.method == 'POST':

        load=json.loads(request.body)

        first_name=load.get('first_name')
        last_name=load.get('last_name')
        username = load.get('username')
        email = load.get('email')
        password = load.get('password')
        age = load.get('age')
        gender = load.get('gender')
        contact = load.get('contact')
        address = load.get('address')

        qualification=load.get('qualification')
        department_id=load.get('department_id')
        doctorFee=load.get('doctorFee')

        if username is None or email is None or first_name is None or last_name is None or password is None or age is None or gender is None or contact is None or address is None or qualification is None or department_id is None or doctorFee is None:
            return JsonResponse({'messge':'Missing any key'},status=400)
        

        if not username or not email or not password or not first_name or not last_name or not age or not gender or not contact or not address or not qualification or not department_id or not doctorFee : 
            return JsonResponse({'message':'Mising Required fields'},status=400)
        else:
            if not re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',email):
                return JsonResponse({'message':'Match Your email Requirements'},status=400)
            
            elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$",password):
                return JsonResponse({'message':'Match Your Password Requirements'},status=400)
        
            else:
                if User.objects.filter(username=username).exists():
                    return JsonResponse({'message':'Username Already exists'},status=409)
                elif User.objects.filter(email=email).exists():
                    return JsonResponse({'message':'Email Already exists'},status=409)
                else:
            
                    user= User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password,age=age,gender=gender,contact=contact,address=address)
                    doctor_role, created = Role.objects.get_or_create(name='Doctor')
                    Doctor.objects.create(qualification=qualification,department_id=department_id,doctorFee=doctorFee,user_id=user.id)
                    if created:
                        return JsonResponse({'message':'You Already Have This Role'})
                    else:
                        user.roles.add(doctor_role)
                        return JsonResponse({'message':'Doctor is Registered Now'},status=201)

    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)
    


def register_user(request):
    if request.method == 'POST':

        load=json.loads(request.body)

        first_name=load.get('first_name')
        last_name=load.get('last_name')
        username = load.get('username')
        email = load.get('email')
        password = load.get('password')
        age = load.get('age')
        gender = load.get('gender')
        contact = load.get('contact')
        address = load.get('address')
        
        
        if username is None or email is None or first_name is None or last_name is None or password is None or age is None or gender is None or contact is None or address is None:
            return JsonResponse({'messge':'Missing any key'},status=400)

        if not username or not email or not password or not first_name or not last_name or not age or not gender or not contact or not address:
            return JsonResponse({'message':'Mising Required fields'},status=400)
        else:
            if not re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',email):
                return JsonResponse({'message':'Match Your email Requirements'},status=400)
            
            elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$",password):
                return JsonResponse({'message':'Match Your Password Requirements'},status=400)
        
            else:
                if User.objects.filter(username=username).exists():
                    return JsonResponse({'message':'Username Already exists'},status=409)
                elif User.objects.filter(email=email).exists():
                    return JsonResponse({'message':'Email Already exists'},status=409)
                else:
                    user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password,age=age,gender=gender,contact=contact,address=address)
                    patient_role, created = Role.objects.get_or_create(name='Patient')
                    
                    if created:
                        return JsonResponse({'message':'You Already Have This Role'})
                    else:
                        user.roles.add(patient_role)

                    return JsonResponse({'message':'User is Registered Now'},status=201)
                    

    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)



def login_user(request):
    
    if request.method == 'POST':

        load=json.loads(request.body)
        username = load.get('username')
        password = load.get('password')
        user=authenticate(username=username,password=password)
        
        if username is None or password is None:
            return JsonResponse({'message': 'Missing any Key.'}, status=400)
        
        if not username or not password:
            return JsonResponse({'message': 'Missing Required field.'}, status=400)
        
        if user is not None:
            login(request,user)

            role =Role.objects.get(user=request.user.id)
            # return JsonResponse({'message':'You Are logged in','role':role.name})
            if not role:
                return JsonResponse({'message':'Yo Not Have Any role'})
            else:
                return JsonResponse({'message':'You Are logged in','role':role.name})
            
        else:
            return JsonResponse({'message':'Incorrect Username Or password'},status=401)
        
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)
        


def logout_user(request):   
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message':'Logged Out Succesfully'},status=204)
        else:
            return JsonResponse({'message':'User Is Not Authenticated'},status=401) 
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)
    


# ----------------------------------------------------- Receptionist Dashboard -----------------------------------------------


def get_patient_appointment(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if Role.objects.filter(user=request.user.id,name="Receptionist").exists():
                patient = list(Appointment.objects.filter(approvedby_receptionist=False,approvedby_doctor=False,deleted_status=False).values('user__first_name','user__last_name','user__age','user__gender','appointmentDate','time','doctor_name','payment_status','department__departments'))

                if patient:
                    return JsonResponse(patient,safe=False)
                else:
                    return JsonResponse({'message': 'No Appointment at this Moment'},status=204) 
            else:
                return JsonResponse({'message': 'You Are Not Autherised'},status=403)   
        else:
            return JsonResponse({'message': 'User not logged in'},status=401)
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)     
    


def approve_appointment(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if Role.objects.filter(user=request.user.id,name="Receptionist").exists():

                load=json.loads(request.body)

                appointment_id=load['appointment_id']
                doctor_id=load['doctor_id']
            

                if not appointment_id or not doctor_id:
                    return JsonResponse({'messege':'Missing Required Field'},status=400)
            

                appointment=Appointment.objects.get(pk=appointment_id)

                if not appointment.approvedby_receptionist:
                    appointment.approvedby_receptionist=True
                    appointment.doctor_id=doctor_id
                    appointment.save()
                
                    return JsonResponse({'messege':'appointment is Approved by Receptionist and doctor is assigned'},status=200)
                else:
                    return JsonResponse({'messege':'You have Already approved this patient'},status=409)
            else:
                return JsonResponse({'messege':'You are not Autherised to make changes'},status=403)
        else:
                return JsonResponse({'messege':'You are not Authenticated'},status=401)
        
    
    
    elif request.method == 'DELETE':
        if request.user.is_authenticated and request.user.is_superuser:

            load=json.loads(request.body)

            appointment_id=load['appointment_id']
            

            if not appointment_id :
                return JsonResponse({'messege':'Missing Required Field'},status=400)
            

            appointment=Appointment.objects.get(pk=appointment_id)

            if appointment.approvedby_receptionist:
                appointment.approvedby_receptionist=False
                appointment.save()

                user = User.objects.get(pk=appointment.user_id)
            

                subject = 'Rejection of Your Appointment'
                rejection_message = f"Dear {user.first_name},\n\n" \
                    f"We regret to inform you that your requested appointment, for {appointment.appointmentDate} has been canceled.\n\n" \
                    f"The cancellation was initiated by our receptionist because of bussy schedule of our doctors. We understand that this may cause inconvenience, and we sincerely apologize for any disruption to your plans.\n\n" \
                    f"If you have any questions or would like to reschedule your appointment, please don't hesitate to contact our reception desk at 9580395130 or reply to email - nikhilsinghj80@gmail.com .We will do our best to accommodate your needs and preferences.\n\n" \
                    f"Once again, we apologize for any inconvenience this may have caused and appreciate your understanding in this matter. We look forward to the opportunity to serve you in the future.\n\n" \
                    f"Thank you for choosing HealthCare."
                from_email = 'nikhilsinghj80@gmail.com'
                to_email = [user.email]
                send_mail(subject, rejection_message, from_email, to_email,fail_silently=False)
                return JsonResponse({'messege':'appointment is Rejected by Receptionist'},status=200)
            else:
                return JsonResponse({'messege':'You have Already Rejected this Appointment'},status=409)
        else:
                return JsonResponse({'messege':'You are not Authenticated'},status=401)
            

    else:
        return JsonResponse({'messege':'Invalid request method'},status=400)
    

def patient_undertrial(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if Role.objects.filter(user=request.user.id,name="Receptionist").exists():
                patient = list(Appointment.objects.filter(approvedby_receptionist=False,approvedby_doctor=False).values())
    
                if patient:
                    return JsonResponse(patient,safe=False)
                else:
                    return JsonResponse({'message': 'No Appointment at this Moment'},status=204) 
            else:
                return JsonResponse({'message':'You Are Not Autherised'},status=403)
        else:
            return JsonResponse({'message': 'User not Autenticated'},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)



def available_doctor(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if Role.objects.filter(user=request.user.id,name="Receptionist").exists():
                doctors = list(Doctor.objects.filter(deleted_status=False).order_by('user__date_joined').values('user','user__first_name','user__last_name','user__age','user__gender','user__contact','department__departments','qualification'))
    
                if doctors:
                    return JsonResponse(doctors,safe=False)
                else:
                    return JsonResponse({'message': 'You are not rgistered '},status=204) 
            else:
                return JsonResponse({'message': 'You Are not Autherised '},status=403)
        else:
            return JsonResponse({'message': 'You Are not Authenticated '},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)


def doctor_full_detail(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            doctor_id=request.GET.get('doctor_id')
            if Role.objects.filter(user=request.user.id,name="Receptionist").exists():
                doctors = list(Doctor.objects.filter(deleted_status=False,user=doctor_id).values('user__first_name','user__last_name','user__age','user__gender','user__contact','department__departments','qualification'))
    
                if doctors:
                    return JsonResponse(doctors,safe=False)
                else:
                    return JsonResponse({'message': 'You are not rgistered '},status=204) 
            else:
                return JsonResponse({'message': 'You Are not Autherised '},status=403)
        else:
            return JsonResponse({'message': 'You Are not Authenticated '},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)



def patient_under_doctor(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            load=json.loads(request.body)
            doctor_id=load['doctor_id']

            if doctor_id is None:
                return JsonResponse({'message': 'Missing any Key'},status=400)

            if not doctor_id:
                return JsonResponse({'message': 'Missing Required Fields'},status=400)
            
            patient = list(Appointment.objects.filter(doctor_id=doctor_id).order_by('appointmentDate').values('user__first_name','user__last_name','user__age','user__gender','user__blood_group','approvedby_doctor','checkup_status','payment_status'))

            if patient:
                return JsonResponse(patient,safe=False)
            else:
                return JsonResponse({'message': 'You are not rgistered '},status=204) 
        else:
            return JsonResponse({'message': 'You Are not autherised '},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)





# ----------------------------------------------------- Doctor Dashboard -----------------------------------------------


def get_unapproved(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            patient = list(Appointment.objects.filter(approvedby_receptionist=True,approvedby_doctor=False).values('pk','user__first_name','user__last_name','user__age','user__gender','appointmentDate','time'))

            if patient:
                return JsonResponse(patient,safe=False)
            else:
                return JsonResponse({'message': 'You have no patient to approve'},status=204) 
        else:
            return JsonResponse({'message': 'User not logged in'},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)
    

def checked(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
            patient = list(Appointment.objects.filter(checkup_status=True).values())

            if patient:
                return JsonResponse(patient,safe=False)
            else:
                return JsonResponse({'message': 'You have not cheked any patient yet'},status=204) 
        else:
            return JsonResponse({'message': 'User not logged in'},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)

def prescribe(request):
    if request.user.is_authenticated:
        if Role.objects.filter(user=request.user.id,name="Doctor").exists():
            load=json.loads(request.body)

            user_id=load.get('user_id')
            medicine=load.get('medicine')
            dosage=load.get('dosage')
            
            if user_id is None or medicine is None or dosage is None:
                return JsonResponse({'message':'Missing any Key'},status=400)
            if not user_id or not medicine or not dosage:
                return JsonResponse({'message':'Missing Required Fields'},status=400)





def confirm_appointment(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            if Role.objects.filter(user=request.user.id,name="Doctor").exists():

                load=json.loads(request.body)
    
                appointment_id=load.get('appointment_id')
    
                if appointment_id is None:
                    return JsonResponse({'message':'Missing any Key'},status=400)            
    
                if not appointment_id :
                    return JsonResponse({'messege':'Missing Required Field'},status=400)
                
    
                appointment=Appointment.objects.get(pk=appointment_id)
    
                if not appointment.approvedby_doctor:
                    appointment.approvedby_doctor=True
                    appointment.save()
    
                    user = User.objects.get(pk=appointment.user_id)
                    department=Dropdown.objects.get(pk=appointment.department_id)
                    doctor=User.objects.get(pk=request.user.id)
                    context={
                                "username":user.first_name,
                                "appointmaentDate":appointment.appointmentDate,
                                "appointmenttime":appointment.time,
                                "doctor":doctor.first_name + ' ' + doctor.last_name,
                                "department":department
                            }
                    
                    
                    confirmation_message = render_to_string('appointment_confirmation.html',context)
                    subject = 'Appointment Confirmation'
                    from_email = 'nikhilsinghj80@gmail.com'
                    to_email = [user.email]
                    send_mail(subject, confirmation_message, from_email, to_email,fail_silently=False,html_message=confirmation_message)
                    return JsonResponse({'messege':'appointment is Approved by Doctor'},status=200)
                else:
                    return JsonResponse({'messege':'You have Already approved this patient'},status=409)
            else:
                return JsonResponse({'message':'You Are Not Autherised'},status=403)    

        else:
                return JsonResponse({'messege':'You are not Authenticated'},status=401)  

         
    
    
    elif request.method == 'PUT':
        if request.user.is_authenticated:
            if Role.objects.filter(user=request.user.id,name="Doctor").exists(): 
                load=json.loads(request.body)

                appointment_id=load.get('appointment_id')
                new_appointmentDate=load.get('new_appointmentDate')
                new_time=load.get('new_time')
                reason=load.get('reason')
                
                
                if appointment_id is None or new_appointmentDate is None or new_time is None or reason is None:
                    return JsonResponse({'messege':'Missing any Key'},status=400)
    
                if not appointment_id or not new_appointmentDate or not new_time or not reason:
                    return JsonResponse({'messege':'Missing Required Field'},status=400)
                
    
                appointment=Appointment.objects.get(pk=appointment_id)
    
                if appointment.approvedby_receptionist:
                    appointment.appointmentDate=new_appointmentDate
                    appointment.time=new_time
                    appointment.save()
    
                    user = User.objects.get(pk=appointment.user_id)
                
                    doctor=User.objects.get(pk=request.user.id)
                    department=Dropdown.objects.get(pk=appointment.department_id)
                    
                    
                    context={
                                # "username":user.first_name,
                                "appointmaentDate":appointment.appointmentDate,
                                "appointmenttime":appointment.time,
                                "doctor":doctor.first_name + ' ' + doctor.last_name,
                                "department":department.departments,
                                "new_appointmentdate":new_appointmentDate,
                                "new_time":new_time,
                                "reason":reason
                            }
                    
                    
                    rejection_message = render_to_string('appointment_reshedule.html',context)
                    subject = 'Appointment Recheduled'
                    from_email = 'nikhilsinghj80@gmail.com'
                    to_email = [user.email]
                    send_mail(subject, rejection_message, from_email, to_email,fail_silently=False,html_message=rejection_message)
                    
                    return JsonResponse({'message':'You Rescheduled This Appointment'})
                else:
                    return JsonResponse({'messege':'Not Approved by Receptionist'},status=200)    
            else:
                return JsonResponse({'message':'You are not Autherised'},status=403)  
        else:
                return JsonResponse({'messege':'You are not Authenticated'},status=401)    
    
    
    
    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            if Role.objects.filter(user=request.user.id,name="Doctor").exists():

                load=json.loads(request.body)
    
                appointment_id=load.get('appointment_id')
                reason=load.get('reason')
                
                if appointment_id is None:
                    return JsonResponse({'messege':'Missing key appointment_id'},status=400)
                if not appointment_id :
                    return JsonResponse({'messege':'Missing Required Field'},status=400)
                
    
                appointment=Appointment.objects.get(pk=appointment_id)
    
                if not appointment.deleted_status:
                    if appointment.approvedby_doctor:
                        return JsonResponse({'messege':'You Can not reject this Appointment As You have Approved It Earlier'},status=403)
                    else:
                        appointment.deleted_status=True
                        appointment.save()
                    
                        user = User.objects.get(pk=appointment.user_id)
                    
                        doctor=User.objects.get(pk=request.user.id)
                        department=Dropdown.objects.get(pk=appointment.department_id)
                        
                        
                        context={
                                
                                    "appointmaentDate":appointment.appointmentDate,
                                    "reason":reason,
                                    "doctor":doctor.first_name + ' ' + doctor.last_name,
                                    "department":department.departments,
                                   
                                }
                        
                        
                        rejection_message = render_to_string('appointment_reject.html',context)
                        subject = 'Appointment Rejection'
                        from_email = 'nikhilsinghj80@gmail.com'
                        to_email = [user.email]
                        send_mail(subject, rejection_message, from_email, to_email,fail_silently=False,html_message=rejection_message)
                        return JsonResponse({'messege':'appointment is Rejected by Doctor'},status=200)
                else:
                    return JsonResponse({'messege':'You Have Already Rejected this Appointment'},status=409)
            else:
                return JsonResponse({'message':'You Are Not Autherised'},status=403)
        else:
                return JsonResponse({'messege':'You are not Authenticated'},status=401) 
                    
    else:
        return JsonResponse({'messege':'Invalid request method'},status=400)



def personal_information(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            doctor = list(Doctor.objects.filter(user_id=request.user.id).values('user__first_name','user__last_name','user__age','user__gender','user__contact','user__address','department__departments','qualification','doctorFee'))

            if doctor:
                return JsonResponse(doctor,safe=False)
            else:
                return JsonResponse({'message': 'You are not rgistered '},status=204) 
        else:
            return JsonResponse({'message': 'You Are not logged in'},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)


def get_approved(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            patient = list(Appointment.objects.filter(approvedby_receptionist=True,approvedby_doctor=True).values('user','user__first_name','user__last_name','user__age','user__gender','appointmentDate','checkup_date'))
            if patient:
                return JsonResponse(patient,safe=False)
            else:
                return JsonResponse({'message': 'You have no patient to approve'},status=204) 
        else:
            return JsonResponse({'message': 'User not logged in'},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)


def get_medicalhistory(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            id= request.GET.get('id')
     
            patient=Medicalhistory.objects.filter(user=id).values()
            if patient:
                return JsonResponse(list(patient),safe=False)
            else:
                return JsonResponse({'message':'Patient Has Not Filled Medical History'},status=204)
            
        else:
            return JsonResponse({'message','You Are Not Authenticted'},status=401)
        
    else:
        return JsonResponse({'message':'Invalid Request Method'},status=400)


# ----------------------------------------------------- Patient Dashboard -----------------------------------------------



def book_appointment(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            
            load=json.loads(request.body)

            appointmentDate = load.get('appointmentDate')
            department_id = load.get('department_id')
            doctor_name = load.get('doctor_name')
            time = load.get('time')

            if appointmentDate is None or department_id is None or time is None or doctor_name is None: 
                return JsonResponse({'message':'Missing any key'},status=400)

            if not appointmentDate or not department_id or not time or not doctor_name: 
                return JsonResponse({'message':'Missing required Field'},status=400)
            
            # print(request.user)
            if Appointment.objects.filter(user=request.user.id,appointmentDate=appointmentDate).exists():
                # print(request.user)
                if Appointment.objects.filter(user_id=request.user.id,department_id=department_id,time=time).exists():
                    return JsonResponse({'message':f'You Already have an appointment on : {appointmentDate} for : {department_id} '},status=409)
                else:
                    Appointment.objects.create(user_id=request.user.id,appointmentDate=appointmentDate,department_id=department_id,doctor_name=doctor_name,time=time)
                    
                    return JsonResponse({'message':'Your appointment is Done'},status=201)
            
            else:
                Appointment.objects.create(user_id=request.user.id,appointmentDate=appointmentDate,department_id=department_id,doctor_name=doctor_name,time=time)
                
                return JsonResponse({'message':'Your appointment is Done'},status=201)
            
                
        else:
            return JsonResponse({'message':'User Is Not Authenticated'},status=401)

    else:
            return JsonResponse({'message':'Invalid request method'},status=400)  
    


def get_patient(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if Role.objects.filter(user=request.user.id,name="Patient").exists():
                patient = list(User.objects.filter(pk=request.user.id).values('first_name','last_name','age','gender','contact','address'))

                if patient:
                    return JsonResponse(patient,safe=False)
                else:
                    return JsonResponse({'message': 'You are not rgistered '},status=204) 
            else:
                return JsonResponse({'message':'you Are Not Autherised'},status=403)
        else:
            return JsonResponse({'message': 'You Are not logged in'},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)



def get_previous_appointments(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            patient = list(Appointment.objects.filter(user_id=request.user.id,deleted_status=False).values('appointmentDate','department__departments','checkup_status','doctor_name','payment_status'))

            if patient:
                return JsonResponse(patient,safe=False)
            else:
                return JsonResponse({'message': 'You have no appointments'},status=204) 
        else:
            return JsonResponse({'message': 'You Are not logged in'},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)


def medical_history(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            load=json.loads(request.body)
           
            blood_group=load.get('blood_group')
            height=load.get('height')
            weight=load.get('weight')
            alcoholic=load.get('alcoholic')
            smoker=load.get('smoker')
            symptoms=load.get('symptoms')
 
            if blood_group is None or height is None or weight is None or alcoholic is None or smoker is None or symptoms is None:
                 return JsonResponse({'message':'Missing any key'},status=400)
            if not blood_group  or not height  or not weight or not alcoholic  or not smoker  or not symptoms :
                 return({'messege':'Missing Required field'})
            if Medicalhistory.objects.filter(user_id=request.user.id).exists():
                return JsonResponse({'message':'You Already have filled Your Medical History'})
            else:
                Medicalhistory.objects.create(user_id=request.user.id,blood_group=blood_group,height=height,weight=weight,alcoholic=alcoholic,smoker=smoker,symptoms=symptoms)
                return JsonResponse({'message':'Your Medical history is saved'},status=201)

        else:
            return JsonResponse({'message': 'You Are not logged in'},status=401) 

    
            
    
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)


# ----------------------------------------------------- Home Page -----------------------------------------------

def dropdown_department(request):
    if request.method == 'GET':
        
        drop = list(Dropdown.objects.filter(deleted_status=False).order_by('departments').values('id','departments'))

        if drop:
            return JsonResponse(drop,safe=False)
        else:
            return JsonResponse({'message': 'Nothing to Show'},status=204) 
           
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)



def dropdown_doctor(request):
    if request.method == 'GET':
        # load=json.loads(request.body)
        # request.GET.get('id')
        department_id = request.GET.get('department_id')
        
        # department_id=load['department_id']
        doctor = list(Doctor.objects.filter( department=department_id,deleted_status=False).values('user__first_name', 'user__last_name','user_id'))

        if doctor:
            
            return JsonResponse(doctor,safe=False)
        else:
            return JsonResponse({'message': 'Nothing to Show'},status=204) 
           
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)


def left_panel(request):
    if request.method=="GET":
        if request.user.is_authenticated:
            if Role.objects.filter(user=request.user.id,name="Receptionist").exists():
                panels=Leftpanel.objects.filter(role="3").values('panel','icons','state')
                if panels:
                    return JsonResponse(list(panels),safe=False)
                else:
                    return JsonResponse({'message':'No Content'},status=204)
            elif Role.objects.filter(user=request.user.id,name="Doctor").exists():
                panels=Leftpanel.objects.filter(role="1").values('panel','icons','state')
                if panels:
                    return JsonResponse(list(panels),safe=False)
                else:
                    return JsonResponse({'message':'No Content'},status=204)
            elif Role.objects.filter(user=request.user.id,name="Patient").exists():
                panels=Leftpanel.objects.filter(role="2").values('panel','icons','state')
                if panels:
                    return JsonResponse(list(panels),safe=False)
                else:
                    return JsonResponse({'message':'No Content'},status=204)
            else:
                return JsonResponse({'message':'No Role Found for this user'},status=304)

        else:
            return JsonResponse({'message':'You are not logged in'},status=401)
        
    else:
        return JsonResponse({'message':'Invalid request Method'},status=400)












            
# ----------------------------------------------------- PDF -----------------------------------------------


def generate_pdf(request):

    if request.method == "POST":
        if request.user.is_authenticated :
            load=json.loads(request.body)
            appointment_id =load.get('appointment_id')
            if appointment_id is None:
                return JsonResponse({'message':'Missing key appointment_id'})
            if not appointment_id:
                return JsonResponse({'message':'Missing Required Field'})
            appointment=Appointment.objects.get(pk=appointment_id)
            doctor=Doctor.objects.get(pk=appointment.doctor_id)
            department=Dropdown.objects.get(pk=appointment.department_id)
            # date=appointment.appointmentDate

            context={
                  "name":request.user.first_name + ' ' + request.user.last_name,
                  "contact":request.user.contact,
                  "visitdate ":request.user.last_login,
                  "billdate":datetime.today(),
                  
                  "doctorname":appointment.doctor_name,
                  "fees":doctor.doctorFee,
                  "invoiceno":appointment.pk,
                  "time":appointment.time,
                  "department":department.departments
                    }
            pdf_content = render_to_string('bill.html',context)
    
            pdf_response = HttpResponse(content_type='template/pdf')
            pdf_response['Content-Disposition'] = 'filename="sample.pdf"'

    
            pdf_response.write(pdf_content)

            return pdf_response
        else:
            return JsonResponse({'messege':'You are not looged in'},status=401)
    else:
        return JsonResponse({'messege':'Invalid request method'},status=400)









# class LabelsView(PDFView):
#     """Generate labels for some Shipments.

#     A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
#     """
#     template_name = 'my_app/labels.html'

#     def get_context_data(self, *args, **kwargs):
#         """Pass some extra context to the template."""
#         context = super().get_context_data(*args, **kwargs)

#         context['shipments'] = User.objects.filter(
#             batch_id=kwargs['pk'],
#         )

#         return context


# from weasyprint import HTML
# from django.template.loader import get_template


# def generate_pdf(request):
#         html_template = get_template('templates/index.html')
#         pdf_file = HTML(string=html_template).write_pdf()
#         response = HttpResponse(pdf_file, content_type='application/pdf')
#         response['Content-Disposition'] = 'filename="home_page.pdf"'
#         return response


# from io import BytesIO
# from django.http import HttpResponse
# from reportlab.pdfgen import canvas

# def generate_pdf(request):
    
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)
#     p.drawString(100, 750, "Hello world.")
#     p.showPage()
#     p.save()

    
#     buffer.seek(0)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="example.pdf"'
#     response.write(buffer.read())

#     return response






# confirmation_message =f"Dear {user.first_name},\n\n" \
                #                       f"We are pleased to confirm the booking of your appointment at HealthCare. Your appointment details are as follows:\n\n" \
                #                       f"- Appointment Date: {appointment.appointmentDate}\n" \
                #                       f"- Appointment Time: {appointment.time}\n" \
                #                       f"- Doctor: Dr. {doctor.first_name + ' ' + doctor.last_name}\n" \
                #                       f"- Department: {appointment.department}\n\n" \
                #                       f"We look forward to providing you with the best healthcare service possible. If you have any questions or need to make any changes to your appointment, please do not hesitate to contact our reception desk at 9580395130 \n\n" \
                #                       f"Thank you for choosing HealthCare . We value your trust and look forward to seeing you on {appointment.appointmentDate} between {appointment.time}.\n\n" \
                #                       f"Sincerely,\n\n" \
                #                       f"HealthCare\n" \
                #                       f"Email : nikhilsinghj80@gmail.com"



                # user = User.objects.get(pk=appointment.user_id)
            
                # doctor=User.objects.get(pk=doctor_id)

                # subject = 'Appointment Confirmation by receptionist'
                # confirmation_message =f"Dear {user.first_name},\n\n" \
                #                       f"We are pleased to inform you that your appointment is approved by our receptionist and pending to approved by Our Doctor . Your appointment details are as follows:\n\n" \
                #                       f"- Appointment Date: {appointment.appointmentDate}\n" \
                #                       f"- Appointment Time: {appointment.time}\n" \
                #                       f"- Doctor: Dr. {doctor.first_name + ' ' + doctor.last_name}\n" \
                #                       f"- Department: {appointment.department}\n\n" \
                #                       f"Thank you for choosing HealthCare and value your trust.\n\n" \
                #                       f"Sincerely,\n\n" \
                #                       f"HealthCare\n" \
                #                       f"Email : nikhilsinghj80@gmail.com"
                # from_email = 'nikhilsinghj80@gmail.com'
                # to_email = [user.email]
                # send_mail(subject, confirmation_message, from_email, to_email,fail_silently=False)
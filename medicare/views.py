# from django.shortcuts import render

from django.http import JsonResponse
import json
import re
from .models import User,Doctor,Appointment,Dropdown
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail


# ----------------------------------------------------- Registration and login/logout -----------------------------------------------

def register_doctor(request):
    if request.method == 'POST':

        load=json.loads(request.body)

        first_name=load['first_name']
        last_name=load['last_name']
        username = load['username']
        email = load['email']
        password = load['password']
        age = load['age']
        gender = load['gender']
        contact = load['contact']
        address = load['address']
        blood_group = load['blood_group']


        qualification=load['qualification']
        department_id=load['department_id']
        doctorFee=load['doctorFee']

        
        

        if not username or not email or not password or not first_name or not last_name or not age or not gender or not contact or not address or not qualification or not department_id or not doctorFee or not blood_group: 
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
            
                    user= User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password,age=age,gender=gender,contact=contact,address=address,blood_group=blood_group,is_staff=True)
                    Doctor.objects.create(qualification=qualification,department_id=department_id,doctorFee=doctorFee,user_id=user.id)
                    return JsonResponse({'message':'Doctor is Registered Now'},status=201)

    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)
    


def register_user(request):
    if request.method == 'POST':

        load=json.loads(request.body)

        first_name=load['first_name']
        last_name=load['last_name']
        username = load['username']
        email = load['email']
        password = load['password']
        age = load['age']
        gender = load['gender']
        contact = load['contact']
        address = load['address']
        blood_group = load['blood_group']


        if not username or not email or not password or not first_name or not last_name or not age or not gender or not contact or not address or not blood_group:
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
                    User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password,age=age,gender=gender,contact=contact,address=address,blood_group=blood_group)
                    return JsonResponse({'message':'User is Registered Now'},status=201)
                    

    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)



def login_user(request):
    
    if request.method == 'POST':

        load=json.loads(request.body)
        username = load['username']
        password = load['password']
        user=authenticate(username=username,password=password)
       
        if user is not None:
            login(request,user)
            return JsonResponse({'message':'You Are logged in','is_superuser':user.is_superuser,'is_staff':user.is_staff})
            
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
        if request.user.is_authenticated and request.user.is_superuser:
            patient = list(Appointment.objects.values())

            if patient:
                return JsonResponse(patient,safe=False)
            else:
                return JsonResponse({'message': 'No Appointment at this Moment'},status=204) 
        else:
            return JsonResponse({'message': 'User not logged in'},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)     
    


def assign_doctor(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:

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
                user = User.objects.get(pk=appointment.user_id)
            
                doctor=User.objects.get(pk=doctor_id)

                subject = 'Appointment Confirmation by receptionist'
                confirmation_message =f"Dear {user.first_name},\n\n" \
                                      f"We are pleased to inform you that your appointment is approved by our receptionist and pending to approved by Our Doctor . Your appointment details are as follows:\n\n" \
                                      f"- Appointment Date: {appointment.appointmentDate}\n" \
                                      f"- Appointment Time: {appointment.time}\n" \
                                      f"- Doctor: Dr. {doctor.first_name + ' ' + doctor.last_name}\n" \
                                      f"- Department: {appointment.department}\n\n" \
                                      f"Thank you for choosing HealthCare and value your trust.\n\n" \
                                      f"Sincerely,\n\n" \
                                      f"HealthCare\n" \
                                      f"Email : nikhilsinghj80@gmail.com"
                from_email = 'nikhilsinghj80@gmail.com'
                to_email = [user.email]
                send_mail(subject, confirmation_message, from_email, to_email,fail_silently=False)
                return JsonResponse({'messege':'appointment is Approved by Receptionist and doctor is assigned'},status=200)
            else:
                return JsonResponse({'messege':'You have Already approved this patient'},status=409)
        else:
                return JsonResponse({'messege':'You are not Autherised to make changes'},status=401)
        
    
    
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
        if request.user.is_authenticated and request.user.is_superuser:
            patient = list(Appointment.objects.filter(approvedby_receptionist=False,approvedby_doctor=False).values())

            if patient:
                return JsonResponse(patient,safe=False)
            else:
                return JsonResponse({'message': 'No Appointment at this Moment'},status=204) 
        else:
            return JsonResponse({'message': 'User not logged in'},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)



def avialable_doctor(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
            doctors = list(Doctor.objects.filter().order_by('department').values('user__first_name','user__last_name','user__age','user__gender','user__contact','department','qualification'))

            if doctors:
                return JsonResponse(doctors,safe=False)
            else:
                return JsonResponse({'message': 'You are not rgistered '},status=204) 
        else:
            return JsonResponse({'message': 'You Are not autherised '},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)



def patient_under_doctor(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
            
            load=json.loads(request.body)
            doctor_id=load['doctor_id']
            
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
        if request.user.is_authenticated and request.user.is_superuser:
            patient = list(Appointment.objects.filter(approvedby_receptionist=True,approvedby_doctor=False).values())

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



def approve_appointment(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_staff:

            load=json.loads(request.body)

            appointment_id=load['appointment_id']
            

            if not appointment_id :
                return JsonResponse({'messege':'Missing Required Field'},status=400)
            

            appointment=Appointment.objects.get(pk=appointment_id)

            if not appointment.approvedby_doctor:
                appointment.approvedby_doctor=True
                appointment.save()

                user = User.objects.get(pk=appointment.user_id)
            
                doctor=User.objects.get(pk=request.user.id)

                subject = 'Appointment Confirmation'
                confirmation_message =f"Dear {user.first_name},\n\n" \
                                      f"We are pleased to confirm the booking of your appointment at HealthCare. Your appointment details are as follows:\n\n" \
                                      f"- Appointment Date: {appointment.appointmentDate}\n" \
                                      f"- Appointment Time: {appointment.time}\n" \
                                      f"- Doctor: Dr. {doctor.first_name + ' ' + doctor.last_name}\n" \
                                      f"- Department: {appointment.department}\n\n" \
                                      f"We look forward to providing you with the best healthcare service possible. If you have any questions or need to make any changes to your appointment, please do not hesitate to contact our reception desk at 9580395130 \n\n" \
                                      f"Thank you for choosing HealthCare . We value your trust and look forward to seeing you on {appointment.appointmentDate} between {appointment.time}.\n\n" \
                                      f"Sincerely,\n\n" \
                                      f"HealthCare\n" \
                                      f"Email : nikhilsinghj80@gmail.com"
                from_email = 'nikhilsinghj80@gmail.com'
                to_email = [user.email]
                send_mail(subject, confirmation_message, from_email, to_email,fail_silently=False)
                return JsonResponse({'messege':'appointment is Approved by Doctor'},status=200)
            else:
                return JsonResponse({'messege':'You have Already approved this patient'},status=409)
        else:
                return JsonResponse({'messege':'You are not Authenticated'},status=401)  

         
    
    
    elif request.method == 'PUT':
        if request.user.is_authenticated and request.user.is_staff: 
            load=json.loads(request.body)

            appointment_id=load['appointment_id']
            appointmentDate=load['appointmentDate']
            time=load['time']
            

            if not appointment_id or not appointmentDate or not time:
                return JsonResponse({'messege':'Missing Required Field'},status=400)
            

            appointment=Appointment.objects.get(pk=appointment_id)

            if appointment.approvedby_doctor:
                appointment.appointmentDate=appointmentDate
                appointment.time=time
                appointment.save()

                user = User.objects.get(pk=appointment.user_id)
            
                doctor=User.objects.get(pk=request.user.id)
                
                subject = 'Reschedulement of Your Appointment'   
                rescheduling_message = f"Dear {user.first_name},\n\n" \
                                       f"We hope this message finds you well. We understand that sometimes unforeseen circumstances can disrupt your plans, and we are here to assist you. Your previously scheduled appointment with Dr. {doctor.first_name + ' ' + doctor.last_name} in the {appointment.department} department, which was originally set for {appointment.appointmentDate}, has been rescheduled Due to busy schedule of Doctor.\n\n" \
                                       f"Your new appointment details are as follows:\n" \
                                       f"- New Appointment Date: {appointmentDate}\n" \
                                       f"- New Appointment Time: {time}\n\n" \
                                       f"We apologize for any inconvenience caused by the change and appreciate your understanding. If the new appointment date and time are not suitable for you, please contact our reception desk. We will make every effort to find an alternative time that accommodates your schedule.\n\n" \
                                       f"Your health and well-being are our top priorities, and we are committed to providing you with the best care possible. If you have any questions or need further assistance, please do not hesitate to reach out to us.\n\n" \
                                       f"Thank you for choosing HealthCare . We look forward to seeing you at your rescheduled appointment.\n\n"\
                                       f"Contact Reception Desk : 9580395130 \n" \
                                       f"Email : nikhilsinghj80@gmail.com"
                from_email = 'nikhilsinghj80@gmail.com'
                to_email = [user.email]
                send_mail(subject, rescheduling_message, from_email, to_email,fail_silently=False)
                
                return JsonResponse({'message':'Your Appointment is Recheduled'})
            else:
                return JsonResponse({'messege':'You not approved this user Yet'},status=200)      
        else:
                return JsonResponse({'messege':'You are not Authenticated'},status=401)    
    
    
    
    elif request.method == 'DELETE':
        if request.user.is_authenticated and request.user.is_staff:

            load=json.loads(request.body)

            appointment_id=load['appointment_id']
            

            if not appointment_id :
                return JsonResponse({'messege':'Missing Required Field'},status=400)
            

            appointment=Appointment.objects.get(pk=appointment_id)

            if appointment.approvedby_doctor:
                appointment.approvedby_doctor=False
                appointment.save()
                
                user = User.objects.get(pk=appointment.user_id)
            
                doctor=User.objects.get(pk=request.user.id)

                subject = 'Rejection of Your Appointment'
                rejection_message = f"Dear {user.first_name},\n\n" \
                    f"We regret to inform you that your scheduled appointment, which was originally set for {appointment.appointmentDate} with Dr. {doctor.first_name + ' ' + doctor.last_name} in the {appointment.department} department, has been canceled.\n\n" \
                    f"The cancellation was initiated by our doctor because he is not avialable due to some urjent work he is out of station. We understand that this may cause inconvenience, and we sincerely apologize for any disruption to your plans.\n\n" \
                    f"If you have any questions or would like to reschedule your appointment, please don't hesitate to contact our reception desk at 9580395130 or reply to email - nikhilsinghj80@gmail.com .We will do our best to accommodate your needs and preferences.\n\n" \
                    f"Once again, we apologize for any inconvenience this may have caused and appreciate your understanding in this matter. We look forward to the opportunity to serve you in the future.\n\n" \
                    f"Thank you for choosing HealthCare."
                from_email = 'nikhilsinghj80@gmail.com'
                to_email = [user.email]
                send_mail(subject, rejection_message, from_email, to_email,fail_silently=False)
                return JsonResponse({'messege':'appointment is Rejected by Doctor'},status=200)
            else:
                return JsonResponse({'messege':'You have Already Rejected this Appointment'},status=409)
        else:
                return JsonResponse({'messege':'You are not Authenticated'},status=401) 
                    
    else:
        return JsonResponse({'messege':'Invalid request method'},status=400)


# ----------------------------------------------------- Patient Dashboard -----------------------------------------------



def book_appointment(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            
            load=json.loads(request.body)

            appointmentDate = load['appointmentDate']
            department_id = load['department_id']
            doctor_id = load['doctor_id']
            time = load['time']

            if not appointmentDate or not department_id or not time or not doctor_id: 
                return JsonResponse({'messege':'Missing required Field'},status=400)
            
            
            if Appointment.objects.filter(user_id=request.user.id,appointmentDate=appointmentDate).exists():
                if Appointment.objects.filter(user_id=request.user.id,department_id=department_id).exists():
                    return JsonResponse({'messege':f'You Already have an appointment on : {appointmentDate} for : {department_id}'},status=409)
                else:
                    Appointment.objects.create(user_id=request.user.id,appointmentDate=appointmentDate,department_id=department_id,doctor_id=doctor_id,time=time)
                    
                    return JsonResponse({'messege':'Your appointment is Done'},status=201)
            
            else:
                Appointment.objects.create(user_id=request.user.id,appointmentDate=appointmentDate,department_id=department_id,doctor_id=doctor_id,time=time)
                
                return JsonResponse({'messege':'Your appointment is Done'},status=201)
            
                
        else:
            return JsonResponse({'messege':'User Is Not Authenticated'},status=401)

    else:
            return JsonResponse({'messege':'Invalid request method'},status=400)  
    


def get_patient(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            patient = list(User.objects.filter(pk=request.user.id).values('first_name','last_name','age','gender','contact','address','blood_group'))

            if patient:
                return JsonResponse(patient,safe=False)
            else:
                return JsonResponse({'message': 'You are not rgistered '},status=204) 
        else:
            return JsonResponse({'message': 'You Are not logged in'},status=401)   
    
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)



def get_previous_appointments(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            patient = list(Appointment.objects.filter(user_id=request.user.id).values('appointmentDate','department','checkup_status'))

            if patient:
                return JsonResponse(patient,safe=False)
            else:
                return JsonResponse({'message': 'You have no appointments'},status=204) 
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

















            
# ----------------------------------------------------- PDF -----------------------------------------------



from django.http import HttpResponse


# def generate_pdf(request):
#     if request.method == 'POST':
#         pdf_content = "This is the content of my PDF."
    
        
#         html = HTML(string=pdf_content)
    
    
#         pdf = html.write_pdf()
    
    
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'filename="my_pdf.pdf"'
#         return response
#     else:
#         return JsonResponse({'message': 'Invalid request method'}, status=400)







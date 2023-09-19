from django.urls import path
from medicare import views

urlpatterns = [
    
     path('registerdoctor/', views.register_doctor),
     path('departdrop/', views.dropdown_department),
     path('doctordrop/', views.dropdown_doctor),
     path('availdoctors/', views.avialable_doctor),
     path('ptunderdoct/', views.patient_under_doctor),
     path('registeruser/', views.register_user),
     path('login/', views.login_user),
     path('logout/', views.logout_user),
     path('bookappointment/', views.book_appointment),
     path('approveappointment/', views.approve_appointment),
     path('assigndoctor/', views.assign_doctor),
     path('getpatientappointment/', views.get_patient_appointment),
     path('patientundertrial/', views.patient_undertrial),
     path('getunapproved/', views.get_unapproved),
     path('checked/', views.checked),
     path('getpatient/', views.get_patient),
     path('getprappoint/', views.get_previous_appointments),
     path('generatepdf/', views.generate_pdf),

     
  
]
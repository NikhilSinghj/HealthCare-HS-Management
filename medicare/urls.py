from django.urls import path
from medicare import views

urlpatterns = [
    
     path('registerdoctor/', views.register_doctor),
     path('registeruser/', views.register_user),
     path('login/', views.login_user),
     path('logout/', views.logout_user),

     path('departdrop/', views.dropdown_department),
     path('doctordrop/', views.dropdown_doctor),

     path('availdoctors/', views.available_doctor),
     path('doctorfulldetail/', views.doctor_full_detail),
     path('checkedpatient/', views.get_checked_patient),
     path('ptunderdoct/', views.patient_under_doctor),
     path('patientundertrial/', views.patient_undertrial),
     path('approveappointment/', views.approve_appointment),
     path('getpatientappointment/', views.get_patient_appointment),

     path('confirmappointment/', views.confirm_appointment),
     path('getunapproved/', views.get_unapproved),
     path('getapproved/', views.get_approved),
     path('checked/', views.checked),
     path('getpatient/', views.get_patient),
     path('doctorinfo/', views.personal_information),

     path('bookappointment/', views.book_appointment),
     path('getprappoint/', views.get_previous_appointments),
     path('generatepdf/', views.generate_pdf),
     path('medicalhistory/', views.medical_history),
     path('getmedicalhistory/', views.get_medicalhistory),
     # path('doctorname/', views.doctorname),
     
     path('getpanel/', views.left_panel),
  
]
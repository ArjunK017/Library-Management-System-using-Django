from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [

    path('', views.index, name= 'index'),

    path('login/', views.login_view, name='login_view'),

    path('logout/',views.logout_view, name='logout_view'),

    path('register/', views.register, name='register'),

    path('adminpage/', views.admin, name='adminpage'),

    path('student/', views.student, name='student'),

    path('teacher/', views.teacher, name='teacher'),

    path('notification/', views.snotification, name='snotification'),

    path('bookrenewal/', views.bookrenewal, name='bookren'),

    path('about/', views.s_about, name='about'),

    path('fine/', views.s_fine, name='fine'),

    path('reserved/', views.s_reserved, name='reserved'),

    path('borrowedbooks/', views.s_borrowbook, name='borrowbook'),

    path('borrowhistory/', views.s_borrowhistory, name='borrowhistory'),

    path('profile/', views.s_profile, name='profile'),

    path('contact/', views.contact, name='contact'),

    path('bookstatistics/', views.bookstats, name='stats'),

    path('bookupdate/', views.bookupdate, name='update'),

    path('fineimposition/', views.fineimpo, name='fineimpo'),

    path('datamanipulation/', views.datamanip, name='datamanip'),

    path('dashboard/',views.dashboard,name='dashboard'),

    path('addbook/',views.addbook,name='addbook'),

    path('AddBookSubmission/',views.AddBookSubmission,name='AddBookSubmission'),

    path('deletebook/<int:id>',views.deletebook,name='deletebook'),

    path('bookissue/',views.bookissue,name='bookissue'),

    path('returnbook/',views.returnbook,name='returnbook'),

    path('issuebooksubmission/',views.issuebooksubmission,name='issuebooksubmission'),
    
    path('returnbooksubmission/',views.returnbooksubmission,name='returnbooksubmission'),

    path('Search/',views.Search,name='Search'),

    path('Searchstudent/',views.Searchstudent,name='Searchstudent'),

    path('editbookdetails/<int:id>',views.editbookdetails,name='editbookdetails'),

    path('<int:id>/updatedetails/',views.updatedetails,name='updatedetails'),



    path('Rsearch/',views.r_Search,name='r_Search'),


    path('viewissuedbook/',views.viewissuedbook,name='viewissuedbook'),

    path('viewstudents/',views.viewstudents,name='viewstudents'),

    path('bookreserve/',views.bookreserve,name='bookreserve'),

    path('viewreservedbooks/',views.viewreservedbooks, name="viewresbook"),
    
    path('bookreserve/', views.bookreserve, name='viewbookreserve'),

    path('borrowbooksubmission/',views.borrowbooksubmission, name='borrowbooksubmission'),

    path('reservebooksubmission/',views.reservebooksubmission, name='reservebooksubmission'),

    path('R1search/',views.r1_Search,name='r1_Search'),

    path('deleteuser/<str:username>/', views.deleteuser, name='deleteuser'),
    
    path('viewtablebooked/', views.viewtablebooked, name='viewtablebooked'),

    path('book/', views.book_slot, name='book_slot'),


    path('book_review/', views.book_review, name='book_review'),

    path('submit_review/', views.submit_review, name='submit_review'),

    path('review_history/', views.review_history, name='review_history'),



]
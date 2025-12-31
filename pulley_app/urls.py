from django.urls import path
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from . import views

urlpatterns = [
    path("image/", views.detect_pulleys, name="detect_pulleys"),
    path('get_current_temperature/', views.get_current_temperature_view, name='get_current_temperature'),
    path('get_current_location/', views.location_view, name='get_current_location'),
    path('', views.main_view, name='main'),
    path('railway/', views.railway_view, name='railway'),
    path('result_data/', views.result_data_view, name='result_data'),
    path('old_data/', views.all_data_view, name='old_data'),
    path('delete/<int:id>/', views.delete_detections, name='delete'),
    path('result_data_camera/', views.result_data_view_for_camera, name='result_data_camera'),
    path('all_data_camera/', views.all_data_view_for_camera, name='all_data_camera'),
    path('delete_camera/<int:id>/', views.detete_detections_camera, name='delete_camera'),
    
    # path('bookings/', views.bookings_view, name='bookings'),
    path('services/', views.services_view, name='services'),
    path('support/', views.support_view, name='support'),
    path('employee/', views.employees_view, name='employee'),
   
    path('calculator/', views.calculator_view, name='calculator'),
    path('calculator-buttons/', views.calculator_buttons_view, name='calculator_buttons'),
    path('pulley-calculator/', views.pulley_calculator_views, name='pulley_calculator'),
    path('employees/', views.employees_view, name='employees'),
    path('employee-delete/<int:id>/', views.employee_deleteview, name='employee_delete'),
    path('choose-database/', views.chooes_your_database_view, name='choose_database'),
    path('choose-database2/', views.chooes_your_database_view2, name='choose_database2'),
    # path('detect-video/', views.detect_pulleys_video, name='detect_video'),
    path('demo-video/', views.demo_video_view, name='demo_video'),
    
    
    # path("yolo_camera/", views.yolo_camera, name="yolo_camera"),
    # path("video_stream/", views.video_stream, name="video_stream"),
    # path("detection_results/", views.detection_results, name="detection_results"),
    # path("stop_camera/", views.stop_camera, name="stop_camera"),
    # path("", views.index, name="index"),
    path("yolo_camera/", views.yolo_camera, name="yolo_camera"),
    path("forms/", views.forms_view, name="forms"),
    path("video_stream/", views.video_stream, name="video_stream"),
    path("detection_results/",views.detection_results, name="detection_results"),
    path("request_capture/", views.request_capture, name="request_capture"),
    path("stop_camera/", views.stop_camera, name="stop_camera"),
    path("", views.index, name="index"),
    
    
    #downlaod files
    path('download_csv/', views.export_csv, name='download_csv'),
    path('download_excel/', views.export_excel, name='download_excel'),
    path('download_csv1/', views.export_csv1, name='download_csv1'),
    path('download_excel1/', views.export_excel1, name='download_excel1'),
    path('download_pdf/', views.export_pdf, name='download_pdf'),
    
    
    #download for id 
    path('records/<int:record_id>/download-csv/', views.download_record_csv, name='download_record_csv'),
    path('records2/<int:record_id>/download-csv/', views.download_record_csv2, name='download_record_csv2'),
    
]
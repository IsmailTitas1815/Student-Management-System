from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from student_management_app import views
from student_management_app import HodViews
from student_management_app import StaffViews
from student_management_app import StudentViews

urlpatterns = [
    path('demo/',views.showDemoPage, name='demo'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.ShowLoginPage, name='show_login'),
    path('get_user_details', views.GetUserDetails, name="get_user_details"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('doLogin', views.doLogin, name='do_login'),
    path('logout', views.logout_user, name='logout'),
    path('admin_home', HodViews.admin_home, name='admin_home'),
    path('add_staff', HodViews.add_staff, name="add_staff"),
    path('add_course', HodViews.add_course, name="add_course"),
    path('add_student', HodViews.add_student, name="add_student"),
    path('add_subject', HodViews.add_subject, name="add_subject"),
    path('manage_staff', HodViews.manage_staff, name="manage_staff"),
    path('edit_staff/<staff_admin_id>', HodViews.edit_staff, name="edit_staff"),
    path('manage_student', HodViews.manage_student, name="manage_student"),
    path('edit_student/<student_admin_id>',
         HodViews.edit_student, name="edit_student"),
    path('manage_course', HodViews.manage_course, name="manage_course"),
    path('edit_course/<course_id>', HodViews.edit_course, name="edit_course"),
    path('manage_subject', HodViews.manage_subject, name="manage_subject"),
    path('edit_subject/<subject_id>', HodViews.edit_subject, name="edit_subject"),
    
    path('manage_session/', HodViews.manage_session, name="manage_session"),
    
    path('student_feedback_message/', HodViews.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_replied/', HodViews.student_feedback_message_replied, name="student_feedback_message_replied"),
    path('staff_feedback_message/', HodViews.staff_feedback_message, name="staff_feedback_message"),
    path('staff_feedback_message_replied', HodViews.staff_feedback_message_replied,
         name="staff_feedback_message_replied"),

    path('student_leave_view', HodViews.student_leave_view,
         name="student_leave_view"),
    path('staff_leave_view', HodViews.staff_leave_view, name="staff_leave_view"),
    path('student_approve_leave/<str:leave_id>',
         HodViews.student_approve_leave, name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>',
         HodViews.student_disapprove_leave, name="student_disapprove_leave"),
    path('staff_disapprove_leave/<str:leave_id>',
         HodViews.staff_disapprove_leave, name="staff_disapprove_leave"),
    path('staff_approve_leave/<str:leave_id>',
         HodViews.staff_approve_leave, name="staff_approve_leave"),

    path('admin_view_attendance', HodViews.admin_view_attendance,
         name="admin_view_attendance"),
    path('admin_get_attendance_dates', HodViews.admin_get_attendance_dates,
         name="admin_get_attendance_dates"),
    path('admin_get_attendance_student', HodViews.admin_get_attendance_student,
         name="admin_get_attendance_student"),
    
    
    path('admin_profile', HodViews.admin_profile,
         name="admin_profile"),
    path('admin_send_notification_staff', HodViews.admin_send_notification_staff,
         name="admin_send_notification_staff"),
    path('admin_send_notification_student', HodViews.admin_send_notification_student,
         name="admin_send_notification_student"),



    path('check_email_exist', HodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist', HodViews.check_username_exist,
         name="check_username_exist"),


    # staff Url path
    path('staff_home/', StaffViews.staff_home, name="staff_home"),
  
    path('staff_take_attendance/', StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('get_students/', StaffViews.get_students, name="get_students"),
    path('save_attendance_data', StaffViews.save_attendance_data, name="save_attendance_data"),
    
    path('staff_update_attendance/', StaffViews.staff_update_attendance, name="staff_update_attendance"),
    path('get_attendance_dates/', StaffViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student/', StaffViews.get_attendance_student, name="get_attendance_student"),
    path('save_updateattendance_data/', StaffViews.save_updateattendance_data, name="save_updateattendance_data"),

    path('staff_apply_leave/', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_feedback/', StaffViews.staff_feedback, name="staff_feedback"),
    
    path('staff_profile', StaffViews.staff_profile,
         name="staff_profile"),
    path('staff_fcmtoken_save', StaffViews.staff_fcmtoken_save,
         name="staff_fcmtoken_save"),

    # student Url path
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_view_attendance/', StudentViews.student_view_attendance, name="student_view_attendance"),

    path('student_apply_leave/', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_feedback/', StudentViews.student_feedback, name="student_feedback"),
    
    path('student_profile', StudentViews.student_profile,
         name="student_profile"),

    path('student_fcmtoken_save', StudentViews.student_fcmtoken_save,
         name="student_fcmtoken_save"),
    path('firebase-messaging-sw.js', views.showFirebaseJS,
         name="show_firebase_js"),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

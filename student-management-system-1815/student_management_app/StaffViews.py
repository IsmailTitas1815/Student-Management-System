import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from student_management_app.models import *
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages


def staff_home(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    subject_count = subjects.count()

    #unique course list
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        if course not in course_id_list:
            course_id_list.append(course.id)


    #students under staff
    students_count = Students.objects.filter(
        course_id__in=course_id_list).count()

    #Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(
        subject_id__in=subjects).count()


    #Fetch All Approve Leave
    staff = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(
        staff_id=staff.id, leave_status=1).count()

    #Fetch Attendance Data by Subject
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count_per_subject = Attendance.objects.filter(
            subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count_per_subject)
    
    #staff's courses students 
    students_attendance = Students.objects.filter(course_id__in=course_id_list)

    #student total present absent
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(
            status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(
            status=False, student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    return render(request, "staff_template/staff_home_template.html", {"students_count": students_count, "attendance_count": attendance_count, "leave_count": leave_count, "subject_count": subject_count, "subject_list": subject_list, "attendance_list": attendance_list, "student_list": student_list, "present_list": student_list_attendance_present, "absent_list": student_list_attendance_absent})


def staff_take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    return render(request, 'staff_template/staff_take_attendance.html', context={"subjects": subjects, "session_years": session_years})


@csrf_exempt
def get_students(request):
    subject_id = request.POST.get('subject')
    session_year = request.POST.get('session_year')

    subject = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.objects.get(id=session_year)
    students = Students.objects.filter(
        course_id=subject.course_id, session_year_id=session_model)
    list_data = []
    for student in students:
        data_small = {"id": student.admin.id,
                      "name": student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_attendance_data(request):
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    subject_model = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.objects.get(id=session_year_id)
    json_sstudent = json.loads(student_ids)  # json to dictonary
    # print(data[0]['id'])

    try:
        attendance = Attendance(
            subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_model)
        attendance.save()

        for stud in json_sstudent:
            student = Students.objects.get(
                admin=stud['id'])  # key diye value khoja
            attendance_report = AttendanceReport(
                student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_update_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_year_id = SessionYearModel.objects.all()
    return render(request, "staff_template/staff_update_attendance.html", {"subjects": subjects, "session_year_id": session_year_id})


@csrf_exempt
def get_attendance_dates(request):
    subject = request.POST.get('subject')
    subject_obj = Subjects.objects.get(id=subject)
    session_year_id = request.POST.get("session_year_id")
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(
        subject_id=subject_obj, session_year_id=session_year_obj)

    attendance_obj = []
    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(
            attendance_single.attendance_date), "session_year_id": attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id, "name": student.student_id.admin.first_name +
                      " "+student.student_id.admin.last_name, "status": student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_updateattendance_data(request):
    student_ids = request.POST.get("student_ids")
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_sstudent = json.loads(student_ids)

    try:
        for stud in json_sstudent:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(
                student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)

    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_msg = request.POST.get('leave_msg')
        try:
            leave_staff = LeaveReportStaff(
                staff_id=staff_obj, leave_date=leave_date, leave_message=leave_msg, leave_status=0)
            leave_staff.save()

            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))

    return render(request, "staff_template/staff_apply_leave.html", context={"leave_data": leave_data})


def staff_feedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaff.objects.filter(staff_id=staff_obj)

    if request.method == "POST":
        feedback_msg = request.POST.get('feedback_msg')
        try:
            staff_feedback = FeedBackStaff(
                staff_id=staff_obj, feedback=feedback_msg, feedback_reply="")
            staff_feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))

    return render(request, "staff_template/staff_feedback.html", context={"feedback_data": feedback_data})


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staffs.objects.get(admin=customuser)
            staff.address = address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
    return render(request, "staff_template/staff_profile.html", {"user": user, "staff": staff})


def staff_fcmtoken_save(request):
    token = request.POST.get('token')
    try:
        staff = Staffs.objects.get(admin = request.user.id)
        staff.fcm_token = token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")
     
from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)

admin.site.register(AdminHOD)

admin.site.register(Courses)
admin.site.register(Subjects)


admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(FeedBackStudent)
admin.site.register(NotificationStudent)


admin.site.register(Staffs)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackStaff)
admin.site.register(NotificationStaff)

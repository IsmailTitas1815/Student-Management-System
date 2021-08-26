from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout
from .EmailBackEnd import EmailBackEnd
from django.contrib import messages
# Create your views here.


def showDemoPage(request):
    return render(request, 'demo.html', context={})


def ShowLoginPage(request):
    return render(request, 'login.html', context={})


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>MEthod Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(
            request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect(reverse("admin_home"))
            if user.user_type == "2": 
                return HttpResponseRedirect(reverse('staff_home'))
            if user.user_type == '3':
                return HttpResponseRedirect(reverse('student_home'))

        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User: " + request.user.email + "User Type: " + request.user.user_type)
    else:
        return HttpResponse("Please login first")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         'apiKey: "AIzaSyAm03ofR9-wBETAY6yoVcaC-8RYj-urLl0",' \
         'authDomain: "student-management-syste-44d20.firebaseapp.com",' \
         'databaseURL: "https://student-management-syste-44d20-default-rtdb.firebaseio.com",' \
         'projectId: "student-management-syste-44d20",' \
         'storageBucket: "student-management-syste-44d20.appspot.com",' \
         'messagingSenderId: "444049804337",' \
         'appId: "1:444049804337:web:e24fab3803a53fb7955910",' \
         'measurementId: "G-TY5VGX8DK0"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")
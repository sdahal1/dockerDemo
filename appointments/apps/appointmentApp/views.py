from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import *
import bcrypt
import datetime
import time
from django.contrib.sessions.models import Session

today = datetime.date.today()
now = datetime.datetime.now().time().strftime('%-H%M')
# Create your views here.
def index(request):
    return render(request, "appointmentApp/loginReg.html")

def process(request):
    print (request.POST)
    errors = User.objects.validator(request.POST)
    print ("after the errors variable")
    print (errors)
    print ("after printing errors")
    if errors:
        for error in errors:
            print (errors[error])
            messages.error(request, errors[error])
        return redirect('/')
    else:
        print ("at the else in process")
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], email = request.POST['email'], password = hashed_pw, dob = request.POST['date'])
        request.session['id'] = user.id
    return redirect('/appointments')

def login(request):
    login_return = User.objects.login(request.POST)
    print ("printing login return")
    print (login_return)

    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        #messages.success(request, "You have successfully logged in")
        return redirect('/appointments')
    else:
        messages.error(request, login_return['error'])
    return redirect('/')

def logout(request):
    Session.objects.all().delete()
    return redirect('/')


def appointments(request):
    
    if 'id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['id']),
            'date': today,
            'appointment': Appointment.objects.filter(date=today).filter(user_appointments=request.session['id']).order_by('time'),
            'later_appointment': Appointment.objects.filter(user_appointments=request.session['id']).exclude(date=today).order_by('date').order_by('time')
            
        }
        return render(request, "appointmentApp/appointments.html", context)
    else:
        messages.error(request, "you must be logged in first")
        return redirect('/')

def new_appointment(request):
    
    

    
    errors = Appointment.objects.validator(request.POST)
    if len(errors)>0:
        for error in errors:
            messages.add_message(request, messages.ERROR, error)
        return redirect ('/appointments')
    # newdate1 = time.strptime(today, "%d/%m/%Y")
    # newdate2 = time.strptime(request.POST['date'], "%d/%m/%Y")
    # if newdate1 < newdate2:
    #     messages.success(request, "Date must be present or greater")
    # else:
    Appointment.objects.create(task=request.POST['task'], date=request.POST['date'], time=request.POST['time'], status="Pending", user_appointments=User.objects.get(id=request.session['id']))
    return redirect('/appointments')

def update(request, task_id):
    print ("****")
    print (request.method)
    context = {
        'task': Appointment.objects.get(id=task_id),
    }
    return render(request, "appointmentApp/update.html", context)

def change(request, task_id):
    errors = Appointment.objects.validator(request.POST)
    if len(errors)>0:
        for error in errors:
            messages.add_message(request, messages.ERROR, error)
        return redirect (reverse('urlname', args = [task_id]))
    a = Appointment.objects.get(id=task_id)
    print ("request.post for updating it below")
    print (request.POST)
    a.task=request.POST['task']
    a.date=request.POST['date']
    a.time=request.POST['time']
    a.status=request.POST['status']
    a.save()
    return redirect('/appointments')

def delete(request, task_id):
    Appointment.objects.get(id=task_id).delete()
    return redirect('/appointments')
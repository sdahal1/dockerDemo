from django.db import models
import re
import bcrypt
import datetime
import time
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
today = datetime.date.today().strftime('%Y-%m-%d')
now = datetime.datetime.now().time().strftime('%-H%M')
class UserManager(models.Manager):

    def validator(self, postData):
        errors= {}
        print ("**********")
        print (postData['date'])
        #today = datetime.today().strftime('%Y-%m-%d')
        print ("todays date is: ")
        print (today)
        print ("wha")
        if today < postData['date']:
            print ("you cant be from the future")
            errors['date'] = "You cannot be born in the future!"
        if postData['date'] =="":
            print ("invalid date doeeee!!!")
            errors['date']= "please select date of birth"
        if len(postData['name']) < 2:
            errors['name_error'] = "Name must be 2 or more characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        if len(postData['password']) < 8 or len(postData['confirm_password']) < 8:
            errors['pass_length'] = "Password must be 8 or more characters"
        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = "Passwords must match"
        if User.objects.filter(email=postData['email']):
            errors['exists'] = "Email already taken"
        return errors
    
    def login(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['error'] = "Email is not valid"
            return errors
        user_to_check = User.objects.filter(email=postData['email'])
        if len(user_to_check) > 0:
            user_to_check = user_to_check[0]
            if bcrypt.checkpw(postData['password'].encode(), user_to_check.password.encode()):
                user = {"user" : user_to_check}
                return user
            else:
                errors = { "error": "Login Invalid- invalid password!!" }
                return errors
        else:
            errors = { "error": "Login Invalid- email not found" }
            return errors

class AppointmentManager(models.Manager):

    def validator(self, postData):
        
        errors = []
        print ("today is : " , today)
        print ("request.post today is: ", postData['date'])
        if len(postData['task']) < 2:
            errors.append("Task must be at least 2 characters")
        if postData['date'] == "":
            errors.append("You must enter a date")
        elif today > postData['date']:
            errors.append("You can only add tasks to today's date or future dates")
        if postData['time'] == "":
            errors.append("You must enter a time")
        if postData['time'] != "":
            newtoday = datetime.date.today().strftime('%Y%m%d')
            postToday = str(postData['date'].split("-"))
            postTodaystr = "".join(postToday)
            timearry = str(postData['time']).split(":")
            timestring = "".join(timearry)
            timeint = int(timestring)
            nowtimeint = int(now)
            print ("timeint from postdata", timeint)
            print ("nowtimeint from datetime.now ", nowtimeint )
            print ("same date")
            print ("today is ", today)
            print ("postdata[date] is: " , postData['date'])
            if str(today) == str(postData['date']) and timeint < nowtimeint+103:
                # print ("timeint from postdata", timeint)
                # print ("nowtimeint from datetime.now ", nowtimeint )
                # print ("same date")
                # print ("today is ", today)
                # print ("postdata[date] is: " , postData['date'])
                # timearry = str(postData['time']).split(":")
                # timestring = "".join(timearry)
                # timeint = int(timestring)
                # nowtimeint = int(now)
                print ("time must be in future")
                errors.append("time must be in future")
        if len(errors)==0 and list(Appointment.objects.filter(date=postData['date']).filter(time=postData['time'])):
            errors.append("this time and date already has an appointment")
        
        

        return errors



class User(models.Model):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Appointment(models.Model):
    task = models.CharField(max_length=255)
    date = models.DateField(blank=False, null=True, default=False)
    time = models.TimeField()
    CATEGORY_CHOICES = (
            ("Pending", "Pending"),
            ( "Missed", "Missed"),
            ( "Done", "Done"),
            )
    status = models.CharField(max_length=255, choices = CATEGORY_CHOICES)
    user_appointments = models.ForeignKey(User, related_name="appointments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()
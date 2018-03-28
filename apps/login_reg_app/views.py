from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime, localtime
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    return render(request,'login_reg_app/index.html')


def add_user(request):
    errors = User.objects.basic_validator(request.POST)
    print "FROM USER", request.POST
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
    else: 
        myrequest = request.POST

        # need to Bcrypt our password
        hash1 = bcrypt.hashpw( myrequest['password'].encode('utf8') , bcrypt.gensalt())
        user = User.objects.create(first_name=myrequest['first_name'], email=myrequest['email'], password=hash1, hired=myrequest['hired'])
        user.save()
    return redirect('/')


def login(request):
    if request.method == 'POST':
        myrequest = request.POST
        user = User.objects.filter(email=myrequest['email'])
        
        if len(user) == 0:
            errors = {}
            errors['user_not_registered'] = "Your email was never found, please try again!"
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            hash2 = user[0].password
            if bcrypt.checkpw(myrequest['password'].encode('utf8'), hash2.encode('utf8')):
                print "1232345323145"
                request.session['id'] = user[0].id
                request.session['first_name'] = user[0].first_name
                request.session['last_name'] = user[0].last_name
                request.session['email'] = user[0].email
                request.session['hired'] = user[0].hired
                request.session['login'] = True
                return redirect('/dashboard')
            else:
                errors = {}
                errors['no_password_found'] = "Password hasn't match with any that we have here. Please try again!"
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')


def dashboard(request):
    me = User.objects.get(id=request.session['id'])

    data = {
        'user': User.objects.get(id=request.session['id'])
    }

    return render(request, 'login_reg_app/dashboard.html', data)


def logout(request):
    request.session.clear()
    return redirect('/')
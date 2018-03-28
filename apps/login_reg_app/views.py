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
        hash1 = bcrypt.hashpw(myrequest['password'].encode('utf8'), bcrypt.gensalt())
        user = User.objects.create(name=myrequest['name'], alias=myrequest['alias'], email=myrequest['email'], password=hash1, birthday=myrequest['birthday'])
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
                request.session['name'] = user[0].name
                request.session['alias'] = user[0].alias
                request.session['email'] = user[0].email
                request.session['birthday'] = user[0].birthday
                request.session['login'] = True
                return redirect('/quotes')
            else:
                errors = {}
                errors['no_password_found'] = "Password hasn't match with any that we have here. Please try again!"
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')


def quotes(request):

    data = {
        'user': User.objects.get(id=request.session['id']),
        'quote': Quote.objects.all().exclude(users=request.session['id']),
        'mylist': Quote.objects.filter(users=request.session['id'])
    }

    return render(request, 'login_reg_app/quotes.html', data)


def add_quote(request):

    myrequest = request.POST
    u = User.objects.get(id=request.session['id'])
    r = Quote.objects.create(insp=myrequest['insp'], quote_by=myrequest['quote_by'], user=u)
    r.save()

    return redirect('/quotes')

def see_user_posts(request, id):
    num = 0
    counter = list(Quote.objects.filter(user=id))
    
    for i in counter:
        num = num+1

    data = {
        'user': User.objects.get(id=id),
        'quote': Quote.objects.filter(user=id),
        'count': num
    }
    return render(request, 'login_reg_app/posts.html', data)


def remove(request, id):

    u = User.objects.get(id=request.session['id'])
    remove = Quote.objects.get(id=id)
    remove.users.remove(u)

    return redirect('/quotes')


def add_to_list(request, id):

    u = User.objects.get(id=request.session['id'])
    quote = Quote.objects.get(id=id)
    quote.users.add(u)

    return redirect('/quotes')


def logout(request):
    request.session.clear()
    return redirect('/')
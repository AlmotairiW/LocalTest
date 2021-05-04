from django.shortcuts import render, redirect
from .models import *
import bcrypt

# Create your views here.


def index(request):
    return render(request, 'index.html')


def process_user(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    new_pass = bcrypt.hashpw(
        request.POST['pass'].encode(), bcrypt.gensalt()).decode()
    if(request.POST['role'] == '1'):
        new_user = Account.objects.create(
            first_name=fname, last_name=lname, email=email, password=new_pass, is_customer=True)
        this_user = Customer.objects.create(account = new_user)
        
    else:
        new_user = Account.objects.create(
            first_name=fname, last_name=lname, email=email, password=new_pass, is_artist=True)
        this_user = Artist.objects.create(account = new_user)
    request.session['uid'] = this_user.account_id
    return redirect('/sucsess')


def sucsess(request):
    this_account = Account.objects.get( id = request.session['uid'])
    if this_account.account.is_artist:
        this_account = Artist.objects.get( account_id = request.session['uid'])
        context = {
            "this_user": Account.objects.get(id=request.session['uid']),
        }
        return render(request,"sucsess.html", context)
    else: # Customer
        pass


def login(request):

    logged_user = Account.objects.get(email=request.POST['email'])
    if bcrypt.checkpw(request.POST['pass'].encode(), logged_user.password.encode()):
        request.session['uid'] = logged_user.id
        return redirect('/sucsess')

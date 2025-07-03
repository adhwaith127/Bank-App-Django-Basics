from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
import re
from .forms import UserForm
from .models import UserModel
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import ValidationError


namepattern=r"^[A-Za-z]+( [A-Za-z]+)?( [A-Za-z]+)?$"
numberpattern=r"^\d+"
amountpattern=r"^\d+(\.\d{1,2})?$"


def signup(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            accountnumber=form.cleaned_data['accountnumber']
            accountname=form.cleaned_data['accountname']
            accountbalance=form.cleaned_data['accountbalance']
            password1=form.cleaned_data['password']
            password2=form.cleaned_data['confirmpassword']
            if password1==password2:
                if UserModel.objects.filter(accountnumber=accountnumber).exists():
                    return render(request,'signup.html',{'form':form,'message':'Account already present'})
                else:
                    user=UserModel(accountnumber=accountnumber,accountname=accountname,accountbalance=accountbalance)
                    user.set_password(password1)
                    try:
                        user.full_clean()
                    except ValidationError as err:
                        accnumerr=','.join(err.get('accountnumber',None))
                        accnamerr=','.join(err.get('accountname',None))
                        accbalerr=','.join(err.get('accountbalance',None))
                        return render(request,'signup.html',{'form':form,'numbererror':accnumerr,'nameerror':accnamerr,'balanceerror':accbalerr})
                    else:
                        user.save()
                        return redirect('userlogin')
            else:
                return render(request,'signup.html',{'form':form,'message':'Passwords do not match'})
        else:
            return render(request,'signup.html',{'form':form})
    form=UserForm()
    return render(request,'signup.html',{'form':form})

def userlogin(request):
    if request.method=='POST':
        accountnumber=request.POST['accountnumber']
        password=request.POST['password']
        if not accountnumber or not password:
            return render(request,'login.html',{'message':'Please enter account number and password'})
        else:    
            user=authenticate(request,accountnumber=accountnumber,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'message':'Invalid Credentials'})  
    return render(request,'login.html')

@never_cache #to avoid loading home page after logout
@login_required(login_url='userlogin')
def home(request):
    return render(request,'home.html')

@never_cache
@login_required(login_url='userlogin')
def details(request):
    user=request.user
    accountnumber=user.accountnumber
    accountname=user.accountname
    accountbalance=user.accountbalance
    return render(request,'details.html',{'accountnumber':accountnumber,'accountname':accountname,'accountbalance':accountbalance})

@never_cache 
@login_required(login_url='userlogin')
def withdrawal(request):
    if request.method=='POST':
        user=request.user
        accountnumber=user.accountnumber
        accountname=user.accountname
        accountbalance=user.accountbalance 
        withdrawamount=request.POST['withdrawamount']
        accountbalance=float(accountbalance)
        withdrawamount=float(withdrawamount)
        if withdrawamount:
            if withdrawamount>accountbalance:
                return render(request,'withdrawal.html',{'message':f'Insufficient balance.Your Current balance is {accountbalance}','accountnumber':accountnumber,'accountname':accountname,'accountbalance':accountbalance})
            else:
                newbalance=accountbalance-withdrawamount
                user.accountbalance=newbalance
                user.save()
                return render(request,'details.html',{'accountnumber':accountnumber,'accountname':accountname,'accountbalance':newbalance})
        else:
            return render(request,'withdrawal.html',{'accountnumber':accountnumber,'accountname':accountname,'accountbalance':accountbalance,'message':'Please enter withdrawal amount'})
    user=request.user
    accountnumber=user.accountnumber
    accountname=user.accountname
    accountbalance=user.accountbalance
    return render(request,'withdrawal.html',{'accountnumber':accountnumber,'accountname':accountname,'accountbalance':accountbalance})
    

@never_cache
@login_required(login_url='userlogin')
def deposit(request):
    if request.method=='POST':
        user=request.user
        accountnumber=user.accountnumber
        accountname=user.accountname
        accountbalance=user.accountbalance 
        depositamount=request.POST['depositamount']
        accountbalance=float(accountbalance)
        depositamount=float(depositamount)
        if depositamount:
            if depositamount<=0:
                return render(request,'deposit.html',{'message':'Please enter valid deposit amount','accountnumber':accountnumber,'accountname':accountname,'accountbalance':accountbalance})
            else:
                newbalance=accountbalance+depositamount
                user.accountbalance=newbalance
                user.save()
                return render(request,'details.html',{'accountnumber':accountnumber,'accountname':accountname,'accountbalance':newbalance})
        else:
            return render(request,'deposit.html',{'accountnumber':accountnumber,'accountname':accountname,'accountbalance':accountbalance,'message':'Please enter deposit amount'})
    user=request.user
    accountnumber=user.accountnumber
    accountname=user.accountname
    accountbalance=user.accountbalance
    return render(request,'deposit.html',{'accountnumber':accountnumber,'accountname':accountname,'accountbalance':accountbalance})


def userlogout(request):
    logout(request)
    return redirect('userlogin')
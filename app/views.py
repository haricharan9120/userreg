from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def user_login(request):
    if request.method=='POST':
         
         username=request.POST['un']
         password=request.POST['pw']

         PUO=authenticate(username=username,password=password)
         if PUO and PUO.is_active:
            login(request,PUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
         else:
            return HttpResponse('INVALID CREDENTIALS') 


    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))







def registration(request):
    EUFO=UserForm()
    EPFO=ProfileForm()
    d={'EUFO':EUFO,'EPFO':EPFO}
    if request.method=='POST' and request.FILES:
        NMUFDO=UserForm(request.POST)
        NMPFDO=ProfileForm(request.POST,request.FILES)
        if NMUFDO.is_valid() and NMPFDO.is_valid():
            MUFDO=NMUFDO.save(commit=False)
            pw=NMUFDO.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()


            MPFDO=NMPFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail('SENDING MAIL FROM SMTP',
                      'SENT MAIL SUCCESSFULLY',
                      'haricharan9120@gmail.com',
                      [MUFDO.email],
                      fail_silently=False)
            return HttpResponse('REGISTRATION DONE SUCCESSFULLY')
        else:
            return HttpResponse("REGISTRATION NOT DONE")
        

    return render(request,'registration.html',d)


@login_required
def profile_display(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)

@login_required
def change_password(request):
    if request.method == 'POST':
        username=request.session.get('username')
        uo=User.objects.get(username=username)
        neww=request.POST['nw']
        uo.set_password(neww)
        uo.save()
        return HttpResponse('PASSWORD CHANGED SUCCESSFULLY')
    return render(request,'change_password.html')


def reset_password(request):
    if request.method == 'POST':
       un=request.POST['un']
       rw=request.POST['rw']
       RUO=User.objects.filter(username=un)
       if RUO:
           UO=RUO[0]
           UO.set_password(rw)
           UO.save()
           return HttpResponse('PASSWORD RESET DONE SUCCESSFULLY ')
       else:
           return HttpResponse('INVALID DATA')       



    return render(request,'reset_password.html')
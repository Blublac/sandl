from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context 

#index

def index(request):
    return render(request,'user/index.html',{'title':'index'})

#registerration section
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            #mail system
            htmly= get_template('user/Email.html')
            d = {'username':username}
            subject, from_email, to ='welcome', 'Your_email@gmail.com', email
            html_content =htmly.render(d)
            msg = EmailMultiAlternatives(subject,html_content,from_email,[to])
            msg.attach_alternative(html_content,'text/html')
            msg.send()

            messages.success(request,f'Your account has been created¦ Please Login')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html',{'form':form,'title':'register here'})

#login section
def Login(request):
    if request.method =='POST':
        #Authenticationform can also be used

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password= password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f'welcome {username},')
            return redirect ('index')

        else:
            messages.info(request, f'account does not exist, please Sign up')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form, 'title': login})
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
import util
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .util import generate_token
from django.utils.encoding import force_bytes

first_name=None
last_name=None
username=None
email=None
password1=None

# Create your views here.
def login(request):
    
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
          
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            
            return render(request,"crop_prediction.html")
        else:
            messages.info(request,"Invalid credentials...")
            return redirect("login")
    else:
        return render(request,"login.html")
        


def register(request):
    global first_name
    global last_name
    global username
    global email
    global password1
    if request.method=="POST":
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        username=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"USERNAME ALREADY TAKEN")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"EMAILID ALREADY TAKEN")
                return redirect("register")
            else:

                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password1)
                current_site = get_current_site(request)
                email_subject = 'Active your Account'
                message = render_to_string('activation.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                                   }
                                   )

                send_mail(
                    email_subject,
                    message,
                    'ashwinrajendran03042001@gmail.com',
                    [email]
                )
                
                user.delete()
                messages.info(request,'''MAIL HAD BEEN SEND TO YOUR REGISTERED MAILID, 
                PLEASE CLICK ON THE GIVEN LINK TO COMPLETE THE REGISTRATION!!!''')
                return redirect("login")
               
        else:
            messages.info(request,"PASSWORD NOT MATCHED")
            return redirect("register")
    else:
        return render(request,"register.html")
def save_user(request,uidb64=None,token=None):
    user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password1)
    user.save()
    return redirect("login")

def logout(request):
    auth.logout(request)
    return redirect("/")

def crop_recommendation(request):
    if request.method == "POST":
        nitrogen = int(request.POST["Nitrogen"])
        phosphorous = int(request.POST["Phosphorous"])
        potassium = int(request.POST["Potassium"])
        temperature = float(request.POST["Temperature"])
        humidity = float(request.POST["Humidity"])
        ph = float(request.POST["Ph"])
        rainfall = float(request.POST["Rainfall"])
        response = {
            "crop_recommended": util.get_recommended_crop(nitrogen, phosphorous, potassium, temperature, humidity, ph,
                                                          rainfall)
        }
        rcrop=response["crop_recommended"]
        message_crop='Nitrogen :'+str(nitrogen)+"\n"+'Phosphorous :'+str(phosphorous)+"\n"+"Potassium :"+str(potassium)+"\n"+"Temprature :"+str(temperature)+"\n"+'Humidity :'+str(humidity)+"\n"+"Ph :"+str(ph)+"\n"+"Rainfall :"+str(rainfall)
        email_user=request.user.email
        
        send_mail(
            'The Recommended Crop',
            'For '+message_crop+"\n The Recommended Crop is "+rcrop,
            'ashwinrajendran03042001@gmail.com',
            [email_user,]
        )
        return render(request,"crop_prediction.html", {'crop':rcrop})
    else:
        return render(request,"crop_prediction.html")
    
from django.shortcuts import render
from tonia_app.forms import UserForm,UserProfileInfoForm

# Extra Imports for the Login and Logout Capabilities
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout


# Create your views here.

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))



@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")


def user_login(request):

    if request.method=="POST":

        username=request.POST.get("username")
        password=request.POST.get("password")
        user =authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("Account not active!")

        else:
            print ("someone tried to login and failed!")
            print ("username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied! Please try again!")

    else:

        return render (request,"tonia_app/login.html")


def index(request):

    return render(request,'tonia_app/index.html')


def register(request):

    registered = False

    if request.method == "POST":

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm (data=request.POST)


        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid() :


            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture

            if "profile_pic" in request.FILES:

                # If yes, then grab it from the POST form reply
                profile.profile_pic=request.FILES["profile_pic"]

            # Now save model
            profile.save()

            # Registration Successful!
            registered=True
            
        else:

            print(user_form.errors,profile_form.errors)

    else:

        user_form=UserForm()
        profile_form=UserProfileInfoForm()


    return render(request,"tonia_app/registration.html",
                                {"user_form":user_form,
                                "profile_form":profile_form,
                                "registered":registered})

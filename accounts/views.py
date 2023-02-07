from django.shortcuts import get_object_or_404, render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import LogInForm, RegistrationForm, StaffCreationForm, StaffDetailsForm, UserDetailsForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import *
from django.contrib import messages

from .utils import get_user_from_email_verification_token, send_email_verification

User=get_user_model()


#USER REGISTRATION
def register(request):
    #if request is a get request return user registration form
    if request.method=="GET":
        form=RegistrationForm()
        return render(request,'accounts/signup.html',{'form':form})

    #if request is a post request create user
    elif request.method=="POST":
        filled_form=RegistrationForm(request.POST)
        #check if form is valid
        if filled_form.is_valid():

            first_name=filled_form.cleaned_data['first_name']
            last_name=filled_form.cleaned_data['last_name']
            username=filled_form.cleaned_data['username']
            email=filled_form.cleaned_data['email']
            password=filled_form.cleaned_data['password']
             
            #create new user
            new_user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                is_active = False
                )
            
            if send_email_verification(request=request, user = new_user):
                return redirect('signin')
            else:
                new_user.delete()
                return redirect('signup')

        #if form is invalid
        else:
            form=filled_form
            context={
                'form':form
                }
            return render(request,'accounts/signup.html',context)

def verify_email_address(request, uidb64, token):
    user = get_user_from_email_verification_token(uidb64, token)
    if user != None:
        user.is_active = True
        user.save()
        login(request, user)
        
    return redirect('signin')

def log_in(request):
    if request.method=="GET":
        #if request is GET check if user is already logged in
        if request.user.is_authenticated:
            #if logged in redirect
            return redirect('dashboard')
        else:
            #if not logged in return login form
            form=LogInForm()
            context ={
                'form':form
                }
            return render(request,'accounts/signin.html',context)

    
    elif request.method=="POST":
        #if request is a POST log in user
        filled_form = LogInForm(request.POST)
        
        if filled_form.is_valid():

            username=filled_form.cleaned_data['username_or_email']
            password=filled_form.cleaned_data['password']
            
            #check if username and password are correct
            user = authenticate(request, username=username, password=password)

            if user != None:
                #if a user is returned authentication was successful
                #log in the user

                login(request, user)
                try:
                    next = request.GET.get('next')
                except:
                    next = None
                if next is None:
                    return redirect('dashboard')
                else:
                    return redirect(next)
            else:
                #if no user is returned authentication failed
                #add error
                filled_form.add_error(field=None,error='Incorrect username/email or password!')
                form=filled_form
                return render(request,'accounts/signin.html',{'form':form})
        else:
            form=filled_form
            return render(request,'accounts/signin.html',{'form':form})
        

@login_required(login_url='/accounts/signin/')
def dashboard(request):
    context={
        'user':request.user
    }
    return render(request, 'dashboard2.html', context)

@login_required(login_url='/accounts/signin/')
def user_profile(request, username):
    user = User.objects.get(username=username)
    user_details={
        'first_name':user.first_name,
        'last_name':user.last_name,
        'email':user.email,
        'username':user.username,
    }
    if request.method=="POST":
        form_type = request.POST.get('form_type')
        if form_type == "user_details":
            filled_form = UserDetailsForm(
                request.POST,
                initial=user_details,
                instance=user
            )
            if filled_form.has_changed():
                if filled_form.is_valid():
                    filled_form.save()
                    messages.success(request,"User info updated successfully")
                    return redirect('user_profile',username=user.username)                    
                else:
                    context={
                        'user_detail_form':filled_form,
                        'password_change_form':PasswordChangeForm(user = user)
                    }
                    return render(request, 'accounts/userprofile.html', context)
            else:
                filled_form.add_error(field=None,error="No changes were detected")
                context={
                    'user_detail_form':filled_form,
                    'password_change_form':PasswordChangeForm(user = user)
                }
                return render(request, 'accounts/userprofile.html', context)
        elif form_type == "password_change":
            filled_form=PasswordChangeForm(user,request.POST)
            if filled_form.is_valid():
                filled_form.save()
                context={
                    'user_detail_form':UserDetailsForm(initial=user_details),
                    'password_change_form':PasswordChangeForm(user = user)
                }
                return redirect('user_profile',username=user.username)
            else:
                context={
                    'user_detail_form':UserDetailsForm(initial=user_details),
                    'password_change_form':filled_form
                }
                return render(request,'accounts/userprofile.html',context)

    else:
        context={
            'user_detail_form':UserDetailsForm(initial=user_details),
            'password_change_form':PasswordChangeForm(user = user)
        }
        return render(request, 'accounts/userprofile.html', context)

@login_required(login_url='/accounts/signin/')
def password_change(request):
    current_user = User.objects.get(username=request.user.username)

    if request.method=="POST":
        filled_form=PasswordChangeForm(current_user,request.POST)

        if filled_form.is_valid():
            filled_form.save()
            return redirect('dashboard')
        else:
            context = {'form':filled_form}
            return render(request,'accounts/changepassword.html',context)
        
    else:
        form=PasswordChangeForm(user=current_user)
        context = {'form':form}
        return render(request,'accounts/changepassword.html',context)
          
        
def log_out(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='/accounts/signin/')
def staff_members(request):
    user_modal_open = False
    staff = StaffUser.objects.all()
    if request.method=="GET":
        context = {
            'staff_members':staff,
            'add_user_form':StaffCreationForm(),
            'user_modal_open':user_modal_open
        }

    elif request.method=="POST":
        filled_form=StaffCreationForm(request.POST)
        #check if form is valid
        if filled_form.is_valid():

            first_name=filled_form.cleaned_data['first_name']
            last_name=filled_form.cleaned_data['last_name']
            username=filled_form.cleaned_data['username']
            email=filled_form.cleaned_data['email']
            password=filled_form.cleaned_data['password']
             
            #create new user
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                is_staff = True
            )
            StaffUser.objects.create(
                user = new_user,
                designation = filled_form.cleaned_data['designation']
            )
            return redirect('staff_members')
            
        #if form is invalid
        else:
            user_modal_open = True
            context = {
                'staff_members':staff,
                'add_user_form':filled_form,
                'user_modal_open':user_modal_open
            }
    
    return render(request,'accounts/staffusers.html',context)

@login_required(login_url='/accounts/signin/')
def staff_details(request, id):
    staff = get_object_or_404(StaffUser, pk=id)
    staff_members = StaffUser.objects.all()
    staff_details={
        'first_name':staff.user.first_name,
        'last_name':staff.user.last_name,
        'email':staff.user.email,
        'username':staff.user.username,
        'designation':staff.designation
    }
    user_detail_modal_open = True
    if request.method=="GET":
        if request.method=="GET":
            context = {
                'staff_members':staff_members,
                'staff_member':staff,
                'staff_details_form':StaffDetailsForm(initial=staff_details),
                'user_detail_modal_open':user_detail_modal_open,
                'add_user_form':StaffCreationForm()
            }
        return render(request,'accounts/staffusers.html',context)
    else:
        filled_form = StaffDetailsForm(request.POST, initial=staff_details)
        if filled_form.has_changed():
            if filled_form.is_valid():
                for field in filled_form.changed_data:
                    if field == "designation":
                        staff.designation = filled_form.cleaned_data['designation']
                    elif field == "first_name":
                        staff.user.first_name = filled_form.cleaned_data['first_name']
                    elif field == "last_name":
                        staff.user.last_name = filled_form.cleaned_data['last_name']
                    elif field == "email":
                        email_qs=User.objects.filter(email=filled_form.cleaned_data['email'])
                        if email_qs.exists():
                            filled_form.add_error(field='email',error="User with that email already exists")
                        else:
                            staff.user.email = filled_form.cleaned_data['email']
                    elif field == "username":
                        username_qs=User.objects.filter(username=filled_form.cleaned_data['username'])
                        if username_qs.exists():
                            filled_form.add_error(field='username',error="User with that username already exists")
                        else:
                            staff.user.username = filled_form.cleaned_data['username']
                if filled_form.is_valid():
                    staff.save()
                    staff.user.save()
                    context={
                        'staff_details_form':StaffDetailsForm(initial={
                            'first_name':staff.user.first_name,
                            'last_name':staff.user.last_name,
                            'email':staff.user.email,
                            'username':staff.user.username,
                            'designation':staff.designation
                        }),
                        'staff_member':staff,
                        'staff_members':staff_members,
                        'add_user_form':StaffCreationForm(),
                        'user_detail_modal_open':user_detail_modal_open,
                    }
                    return redirect('staff_details',id=staff.id)
                else:
                    context={
                        'staff_details_form':filled_form,
                        'staff_member':staff,
                        'staff_members':staff_members,
                        'add_user_form':StaffCreationForm(),
                        'user_detail_modal_open':user_detail_modal_open,
                    }
                    return render(request,'accounts/staffusers.html',context)
                
            else:
                context={
                    'staff_details_form':filled_form,
                    'staff_member':staff,
                    'staff_members':staff_members,
                    'add_user_form':StaffCreationForm(),
                    'user_detail_modal_open':user_detail_modal_open,
                }
                return render(request,'accounts/staffusers.html',context)
        else:
            filled_form.add_error(field=None,error="No changes were detected")
            context={
                'staff_details_form':filled_form,
                'staff_member':staff,
                'staff_members':staff_members,
                'add_user_form':StaffCreationForm(),
                'user_detail_modal_open':user_detail_modal_open,
            }
            return render(request,'accounts/staffusers.html',context)

@login_required(login_url='/accounts/signin/')
def activate_staff(request, id):
    staff = get_object_or_404(StaffUser, pk=id)
    staff.user.is_active = True
    staff.user.save()
    return redirect('staff_details',id=staff.id)

@login_required(login_url='/accounts/signin/')
def deactivate_staff(request, id):
    staff = get_object_or_404(StaffUser, pk=id)
    staff.user.is_active = False
    staff.user.save()
    return redirect('staff_details',id=staff.id)

@login_required(login_url='/accounts/signin/')
def delete_staff(request, id):
    staff = get_object_or_404(StaffUser, pk=id)
    staff.user.delete()
    return redirect('staff_members')
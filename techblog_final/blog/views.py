from django.shortcuts import render,HttpResponseRedirect, redirect
from .forms import SignUpForm, LoginForm, BlogForm, UpdateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Blog
from django.contrib.auth.models import Group
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from .forms import ContactForm

# Create your views here.
def home(request):
    blogs = Blog.objects.all()
    return render(request,'blog/home.html',{'blogs':blogs})

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"CONGRATULATION, You are Registered!")
            user = form.save()
            try:
                group = Group.objects.get(name='Author')
                user.groups.add(group)
            except Group.DoesNotExist:
                messages.error(request, "Author group does not exist!")
    else:
        form=SignUpForm()
    return render(request,'blog/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request = request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                pwd = form.cleaned_data['password']
                user = authenticate(username=uname, password=pwd)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def dashboard(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.filter(author=request.user) 
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        if blogs.exists():
            return render(request, 'blog/dashboard.html', {'blogs': blogs, 'full_name': full_name, 'groups': gps})
        else:
            # Handle case where there are no blogs for the user (optional)
            return render(request, 'blog/dashboard.html', {'message': 'No blogs found yet!', 'full_name': full_name, 'groups': gps})
    return HttpResponseRedirect('login')  # Redirect to login page if not authenticated
   

def add_blog(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BlogForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                cont = form.cleaned_data['cont']
                blg = Blog(author=request.user, title=title, cont = cont)
                blg.updated_at = timezone.now()
                blg.save()
                form = BlogForm()
                return HttpResponseRedirect('/dashboard/')
        else:
            form = BlogForm()
            return render(request, 'blog/addblog.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def update_blog(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Blog.objects.get(pk=id)
            form = BlogForm(request.POST,instance = pi)
            if form.is_valid():
                pi.updated_at = timezone.now()
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Blog.objects.get(pk=id)
            form = BlogForm(instance=pi)
        return render(request, 'blog/updateblog.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_blog(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Blog.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        # profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid():
            user_form.save()
            # profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        # profile_form = UpdateProfileForm(instance=request.user.profile)
    # print(request.user.profile)
    return render(request, 'blog/profile.html', {'user_form': user_form})

def contact(request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']
                message = f'From: {email}\n\n{message}'
                subject = f'Contact Form Submission from {name}'

                send_mail(
                    subject,
                    message,
                    email,
                    ['kratinmourya09@gmail.com'],  # recipient's email address
                    fail_silently=False,
                )
                messages.success(request, 'Email sent successfully')
                return redirect('/contact')  # Redirect to a thank you or success page

        # If the form is not valid, or if the request method is not POST, re-render the form page.
        form = ContactForm()
        return render(request, 'blog/contact.html', {'form': form})



class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'blog/changepassword.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')
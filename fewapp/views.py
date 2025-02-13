from .models import Category
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Post ,Aboutus
from django. http import Http404
from django.core.paginator import Paginator
from .forms import  LoginForm, PostForm ,Registerform, ResetPasswordForm
from .forms import Contactform, ForgotPasswordForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail


#posts = [
#       {'id':1,'title':'post 1','content':'content of post 1'},
#       {'id':3,'title':'post 3','content':'content of post 3'},
#       {'id':4,'title':'post 5','content':'content of post 5'},
#       {'id':5,'title':'post 6','content':'content of post 7'},
#       {'id':6,'title':'post 7','content':'content of post 8'},
#   ]
def index(request):
    fewapp_title="latest posts"
    #getting data from post model
    all_posts = Post.objects.all()
    
    #paginate            5->how many post your want to show per page
    paginator=Paginator(all_posts,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    return render(request,'index.html',{'fewapp_title': fewapp_title,'page_obj':page_obj})

def detail(request,slug):
    #static data
    #post = next(( item for item in posts if item['id'] == int(post_id)),None)
    try:
    #getting data from model by post id
        post = Post.objects.get(slug=slug)
        related_posts =Post.objects.filter(category=post.category).exclude(pk=post.id)
        
        
    except Post. DoesNotExist: 
        raise Http404("post does not exist!")
    #logger=logging.getLogger("TESTING")
    #logger.debug(f'post variable is {post}')
    return render(request,'detail.html',{'post': post,'related_posts': related_posts})

def myname(request):
    return HttpResponse("my name is logesh")    

def old_url_redirect(request):
    return redirect(reverse('fewapp:new_page_url'))

def new_url_view(request):
    return HttpResponse("this is the new url")

def contact(request):
    if request.method =='POST':
        form = Contactform(request.POST)
        name= request.POST.get('name')
        email= request.POST.get('email')
        message= request.POST.get('message')
        logger=logging.getLogger("TESTING")
        if form.is_valid():
           logger.debug(f'POST datais { form.cleaned_data['name']} { form.cleaned_data['email']} { form.cleaned_data['message']}')
           success_message='your email has been sent!'
           return render(request,'includes/contact.html',{'form':form , 'success_message':success_message })
        else:
            logger.debug('Form validation failure') 
        return render(request,'includes.html',{'form':form , 'name':name ,'email':email,'message':message})    
    return render(request,'contact.html')


def about(request):
    about_content =  Aboutus.objects.first()
    if about_content is None or not about_content.content:
        about_content ="default content goes here." #default text
    else:
        about_content = about_content.content    
    return render(request,'about.html',{'about_content': about_content})

@csrf_exempt
def register(request):
     form = Registerform()    
     if request.method == 'POST':
        form =Registerform(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #user data created
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,'registration successful.you can login ')
            return redirect("fewapp:login")

     return render(request,'register.html',{'form' :form})
 
@csrf_exempt
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        #login form
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data["password"]
            user = authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                return redirect("fewapp:dashboard")#redirect to dashboard
                print("LOGIN SUCCESS")
            else:
                form.add_error(None, "Invalid login credentials")     
    return render(request,'login.html',{'form':form}) 


def dashboard(request):
    fewapp_title= "my posts"
    #getting the user posts
    all_posts = Post.objects.filter(user=request.user)
    
    #paginate            5->how many post your want to show per page
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    return render(request,'dashboard.html',{"fewapp_title":fewapp_title,'page_obj':page_obj})       

def logout(request):
    auth_logout(request)
    return redirect("fewapp:index")

@csrf_exempt
def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        #form
        form=ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user =  User.objects.get(email=email)
            #send email to reset password
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = "reset password requested"
            message = render_to_string('reset_password_email.html',{'domain':domain , 'uid':uid, 'token':token})
            
            send_mail(subject,message,'noreply@jvlcode.com',[email])
            messages.success(request, 'email has been sent',)
            
    return render(request,'forgot_password.html',{'form':form})     
       
def reset_password(request, uidb64, token):
    # Your reset logic here
    form = ResetPasswordForm()
    if request.method == 'POST':
        #form
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            try:
                
               new_password = form.cleaned_data['new_password']
               uid = urlsafe_base64_decode(uidb64)
               user = User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError ,User.DoesNotExist):
                user = None
                
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request,'your password is reset successfully')
                return redirect('fewapp;login')
            else:
                messages.error(request,'the password reset link is invalid')
                    
    return render(request, 'reset_password_email.html',{'form':form})
    
@csrf_exempt   
def new_post(request):
    categories = Category.objects.all()
    form = PostForm()
    if request.method == 'POST':
        #form
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect ('fewapp:dashboard')
    return render(request,'new_post.html',{'categories':categories,'form':form})

def edit_post(request,post_id):
    categories = Category.objects.all()
    return render(request,'edit_post.html', {'categories':categories })
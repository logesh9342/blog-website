from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from .models import Category, Post

class Contactform(forms.Form):
    name = forms.CharField(label='name' ,max_length=100 ,required=True)
    email = forms.EmailField(label='Email',required=True)
    message = forms.CharField(label='message',required=True)
    
class Registerform(forms.ModelForm):
    username= forms.CharField (label='Username', max_length=100 ,required =True)
    email = forms.EmailField(label='Email', max_length=100 ,required= True)   
    password = forms.CharField(label='Password', max_length=100 ,required= True)
    password_confirm = forms.CharField(label='Confirm_Password', max_length=100 ,required= True)
    
    class Meta:
        model = User
        fields =('username','email','password')
        
        
    def clean(self):
        cleaned_data =super().clean()
        password =cleaned_data.get("password")
        password_confirm =cleaned_data.get("password_confirm")
        
        if password and password_confirm and password!=password_confirm:
            raise forms.ValidationError("password doesn't match")    
      
class LoginForm(forms.Form):
    username= forms.CharField (label='Username', max_length=100 ,required =True)     
    password = forms.CharField(label='Password', max_length=100 ,required= True)  
    
    def clean(self):
        cleaned_data =super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username,password=password)
            if user is None:
                raise forms.ValidationError("Invalid username and password") 
         
class ForgotPasswordForm(forms.Form):
    email=forms.EmailField(label='Email',max_length=254 , required=True, )
    
    def clean(self):
        cleaned_data = super() .clean()
        email = cleaned_data.get('email')
        
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("no user regirsterd with this email")            
        
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='New password', min_length=8)
    confirm_password = forms.CharField(label='confirm new password', min_length=8)
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password =cleaned_data.get("confirm_password")
        
        if new_password and confirm_password and new_password!= confirm_password:
            raise forms.ValidationError("password doesn't match")  
        
class PostForm(forms.ModelForm):
    forms.CharField(label='title', max_length=200, required=True)  
    content = forms.CharField(label ='content', required = True)
    category = forms.ModelChoiceField(label='category',required=True, queryset=Category.objects.all())
    img_url = forms.ImageField(label='Image' ,required=False) 
    
    class Meta:
        model = Post
        fields = ['title','content','category','img_url']
        
    def clean(self):
        cleaned_data = super().clean()    
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        
        #custom validation
        if title and  len(title) < 5:
            raise forms.ValidationError('title must be atleast 5 characters long')
        
        if content and len(content) < 10:
            raise forms.ValidationError('content must be atleast 10 characters') 
    
    def save(self, commit = ...):
        post = super().save(commit)    
        cleaned_data = super().clean()    
        
        if cleaned_data.get('img_url'):
            post.img_url = cleaned_data.get('img_url')
        else:    
            img_url="https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
            post.img_url = img_url       
        
        post.img_url = img_url
        if commit:
            post.save()
        return post    
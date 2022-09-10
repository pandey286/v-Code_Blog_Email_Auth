from ast import Return
from turtle import title
from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from random import randrange
from django.contrib.auth.models import User
from blog.models import Post


# Create your views here.

# HTML Pages
def home(request):
    return render(request, 'home/home.html')
   
def about(request):
    return render(request, 'home/about.html')   

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact= Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message have been send successfully")
    return render(request, 'home/contact.html')
    
def search(request):
    # allPosts = Post.objects.all()
    query = request.GET['query']
    if len(query)>50:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent).union(allPostsAuthor)
    
    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)
    

# Authentication APIs
def handleSignup(request):
    if request.method == "POST":
        un = request.POST.get("un")
        try:
            ur = User.objects.get(username=un)
            return redirect("/",{messages.error(request,'User Already Exist')})
        except User.DoesNotExist:
            text = "0123456789"
            pw = ""
            for i in range(4):
                pw = pw + text[randrange(len(text))]
            print(pw)
            ur = User.objects.create_user(username=un,password=pw)
            ur.save()
            send_mail("Welcome to v/Code Blog","your password is " + str(pw),"pandeyprashant953@gmail.com",[str(un)])
            return redirect("/",{messages.info(request,'Your Password is send on your mail')})
    else:
        return redirect("/signup")


def handleLogin(request):
    if request.user.is_authenticated:
        return redirect("/")
    elif request.method == "POST":
        un = request.POST.get("un")
        pw = request.POST.get("pw")
        ur = authenticate(username=un, password=pw)
        if ur is not None:
            login(request, ur)
            return redirect("/")
        else:
            return redirect("/",{messages.error(request,'Invalid Login')})
    else:
        return render(request, "/")

def handlernpassword(request):
	if request.method == "POST":
		un = request.POST.get("un")
		try:
			ur = User.objects.get(username=un)
			text = "0123456789"
			pw = ""
			for i in range(4):
				pw = pw + text[randrange(len(text))]
			print(pw)
			ur.set_password(pw)
			ur.save()
			send_mail("Welcome to v/Code Blog","your new password is " + str(pw),"pandeyprashant953@gmail.com",[str(un)])
			return redirect("/")
		except User.DoesNotExist:
			return redirect("/",{messages.error(request,'User Does Not Exist')})
	else:
		return redirect("/")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('/')


from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
#html pages
def home(request):
    return render(request,'home/home.html')

def about(request):
    messages.success(request,'this is about')
    return  render(request,'home/about.html')

def contact(request):
    if request.method=="POST":
        print('we are using csrf' )  
        name=request.POST['name']    
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']   
        print(name,email,phone,content)
        if len(name)<2 or len(email)<4 or len(phone)<10 or len(content)<10:
            messages.error(request,'Please fill the form correctly')
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,'You massege is successfully sent')
    return render(request,'home/contact.html')    


def search(request):
	query=request.GET['query']
	if len(query)>80:
		allPosts=Post.objects.none()
	else:
		allPostsTitle = Post.objects.filter(title__icontains=query)
		allPostsContent=Post.objects.filter(content__icontains=query)
		allPosts=allPostsTitle.union(allPostsContent) 
	if allPosts.count()==0:
		messages.warning(request,'No search result found. plese refine your query')
	params={'allPosts':allPosts,'query':query}
	return render(request,'home/search.html',params) 

	#authentication APIs

def handlesignup(request):
	if request.method=='POST':
		#get the post parameter
		username=request.POST['username']
		fname=request.POST['fname']
		lname=request.POST['lname']
		email=request.POST['email']
		pass1=request.POST['pass1']
		pass2=request.POST['pass2']
		#check for errorneous input
		#Username must be  under 10 characters
		if len(username) >20:
			messages.error(request,'Username must be  under 20 characters')
			return HttpResponseRedirect('/')
		#Username should only alphanumeric
		if not username.isalnum():
			messages.error(request,'Username should only contain latters and numbers')
			return HttpResponseRedirect('/')

		#Password should match
		if pass1 != pass2:
			messages.error(request,'Password do not match ')
			return HttpResponseRedirect('/')

		#create user
		myuser=User.objects.create_user(username,email,pass1)
		myuser.first_name=fname
		myuser.last_name=lname
		myuser.save()
		messages.success(request,'Your account has been successfully created ')
		return HttpResponseRedirect('/')
	else:
		return HttpResponse('404 - Not Found')

def handlelogin(request):
	if request.method=='POST':
		#get the post parameter
		loginusername=request.POST['loginusername']
		loginpass=request.POST['loginpass']
		user=authenticate(username=loginusername,password=loginpass)
		if user is not None:
			login(request,user)
			messages.success(request,'Successfully Logged In')
			return HttpResponseRedirect('/')
		else:
			messages.error(request,'Invalid Credentials, Please try again')
			return HttpResponseRedirect('/')	
	return HttpResponse('404 - Not Found')

def handlelogout(request):
	logout(request)
	messages.success(request,'Successfullt Logged out')
	return HttpResponseRedirect('/')

	return HttpResponse('handlelogout')

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from blog.models import Post,BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
	allPosts=Post.objects.all()
	context={'allPosts':allPosts}
	return  render(request,'blog/blogHome.html',context)

def blogPost(request,slug):
	post=Post.objects.filter(slug=slug).first()
	comments=BlogComment.objects.filter(post=post,parent=None)
	replies=BlogComment.objects.filter(post=post).exclude(parent=None)
	repDict={}
	for reply in replies:
		if reply.parent.sno not in repDict.keys():
			repDict[reply.parent.sno]=[reply]
		else:
			repDict[reply.parent.sno].append(reply)
	print(repDict)
	context={'post':post,'comments':comments ,'user':request.user,'repDict':repDict}
	return  render(request,'blog/blogPost.html',context)
   
def postcomment(request):
	if request.method=='POST':
		comment=request.POST.get('comment')
		user=request.user
		postSno=request.POST.get('postSno')
		post=Post.objects.get(sno=postSno)
		parentsno=request.POST.get('parentsno')
		if parentsno=='':
			comment=BlogComment(comment=comment,user=user,post=post)
			comment.save()
			messages.success(request,'Your comment has been posted successfully')
		else:
			parent=BlogComment.objects.get(sno=parentsno)
			comment=BlogComment(comment=comment,user=user,post=post,parent=parent)
			comment.save()
			messages.success(request,'Your reply has been posted successfully')
		
		
	
	return  HttpResponseRedirect(f'/blog/{post.slug}')
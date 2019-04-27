from django.shortcuts import render,redirect
from .models import Blog,BlogAuthor,BlogComment,Category,Subscribe,BlogReply
from .forms import Comment,subscribe,contact,Reply
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.db.models import Q



def base(request, slug):
    categories = Category.objects.get(slug=slug)
    blogs = Blog.objects.filter(catagory=categories)
    print(blogs)
    context = {
        'blogs':blogs,
    
    }
    return render(request, 'category.html', context)
def base1(request):
    categories = Category.objects.all()
 
    
    context = {
        'cat':categories
    }
    return render(request, 'base.html', context)

def BlogList(request):
    blogs = Blog.objects.all()
    for i in (blogs):
        i.description=i.description[:500]
    context = {
        'blogs':blogs
    }
    return render(request,'bloglist.html',context)

def BlogDetail(request,slug):
    lis   = Blog.objects.all()
    blogs = Blog.objects.get(slug=slug)
    comments= BlogComment.objects.filter(blog=blogs)
    # reply = BlogReply.objects.filter(comment = comments)    
    # print(reply)
    replies = BlogReply.objects.all()
    # print(comments)
    form = Comment()
    form_1 = Reply()
    if request.method =='POST':
         form=Comment(request.POST or None)
         if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.blog=blogs
            new_comment.save()
            form.save()
            return HttpResponseRedirect(reverse('detail', args=[slug]))
             
 
    context = {
        'blogs':blogs,
        'comments':comments,
        'list':lis,
        'form':form,
        # 'relpy' : reply,
        'replies' : replies,
        'form_1' : form_1,
    }
    return render(request,'blogdetail.html',context)


def BlogAuthors(request):
    authors = BlogAuthor.objects.all()
    context = {
        'authors':authors
    }

    return render(request,'authorlist.html',context)

def BlogListByAuthor(request,id):
    target_author  = BlogAuthor.objects.get(id=id)
    print(target_author)
    blogs          = Blog.objects.filter(author=target_author)
    context = {
        'blogs':blogs,
        'author':target_author
    }
    return render(request,'authorblogs.html',context)


# def sub(request):
#     form = subscribe()
#     if request.method == 'POST':
#         form = subscribe(request.POST or None)
#         if form.is_valid():
#             form.save()
#     context = {
#        'form':form,
#    }
    
#     return render(request,'subscribe.html',context)

def Contact(request):
    form = contact()
    subject = 'contact blog'
    if request.method=='POST':
        form = contact(request.POST or None)
        if form.is_valid():
            name=form.cleaned_data.get('Name')
            email=form.cleaned_data.get('Email')
            message = form.cleaned_data.get('Message')
            email_from=email
            send_mail( subject, message, email_from, recipient_list=[settings.EMAIL_HOST_USER] )
            return redirect('list')
    return render(request,'contact.html',{'form':form})



def search(request):

    query=request.GET.get('query',None)
    blogs=Blog.objects.all()
    if query is not None:
        blogs=blogs.filter(
        Q(title__icontains=query)|
        Q(description__icontains=query)|
        Q(catagory__Name__icontains=query)|
        Q(author__author__username__icontains=query)

        )
    context={

        'blogs':blogs
}

    return render(request,'bloglist.html',context)

def sub(request):
    if request.method!='POST':
        form = subscribe()
    
    else:
        form = subscribe(request.POST)
        if form.is_valid():
           form.save()
           current_site = get_current_site(request)
           message = render_to_string('acc_active_email.html', {
                'form':form, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(form)),
                'token': account_activation_token.make_token(form),
            })
           mail_subject = 'Activate your blog account.'
           to_email = form.cleaned_data.get('email').lower()
           email = EmailMessage(mail_subject, message, to=[to_email])
           email.send()
            
           return render(request, 'acc_active_email_confirm.html')
    return render(request, 'subscribe.html', {'form' : form, })

def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
      
        #login(request, user)
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    return redirect('list')
 

def ReplyPage(request,id, slug):
    comment=BlogComment.objects.get(id=id)
 #   reply  = BlogReply.objects.filter(comment=comment)
    #blog = Blog.objects.get()
    #print(reply)
    #print(comment)
    form = Reply()
    #print(form)

    if request.method=='POST':
        form = Reply(request.POST or None)
        if form.is_valid:
            new = form.save(commit=False)
            new.comment=comment
            new.save()
            form.save()
     #       return HttpResponseRedirect(reverse('detail', args=[comment.s])) 
            return HttpResponseRedirect(reverse('detail', args = [slug]))
            # return redirect('list')

            
                
    context={
    #'reply': reply,
    'form1':form,
    'comment': comment,
    'slug' : slug,
    }
    return render(request,'blogReply.html',context)
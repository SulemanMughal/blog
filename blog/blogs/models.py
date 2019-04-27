from django.db import models
from django.conf import settings
from embed_video.fields import EmbedVideoField
from django.db.models.signals import pre_save
from django.dispatch import receiver
# from myapp.models import MyModel
from django.conf import settings
from django.core.mail import send_mail
# from django.dispatch import receiver
# from django.core.signals import post_save
from django.db.models.signals import post_save
import django.dispatch
# from django.contrib.sites.shortcuts import get_current_site
# from django.http import request

# from django.contrib.sites.models import Site


class Category(models.Model):
    Name      =       models.CharField(max_length=500)
    slug      =       models.CharField(max_length=500)
    def __str__(self):
        return self.Name


class BlogAuthor(models.Model):
    author     =       models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    image      =       models.ImageField()
    bio        =       models.TextField(help_text='Write something about you')

    def __str__(self):
        return self.author.username


    

class Blog(models.Model):
    catagory    =       models.ForeignKey(Category,on_delete=models.CASCADE)
    author      =       models.ForeignKey(BlogAuthor, on_delete=models.CASCADE, null=True)
    title       =       models.CharField(max_length=1000)
    slug        =       models.CharField(max_length=1000)
    image       =       models.ImageField(blank=True)
    video       =       EmbedVideoField(blank=True)
    description =       models.TextField()
    created_at  =       models.DateTimeField(auto_now_add=True)
    updated     =       models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    # pizza_done = django.dispatch.Signal(providing_args=["title"])

    # def send_pizza(self, title):
    #     pizza_done.send(sender=self.__class__, toppings=toppings)
        

    # def save(self, *args, **kwargs):
    #     blog = super(Category, self).save(*args, **kwargs)
    #     Blog.objects.get_or_create(id=blog.id)
    #     return 
    
    # def get_absolute_url(self):







class BlogComment(models.Model):
    name        =       models.CharField(max_length=100)
    email       =       models.CharField(max_length=100)
    description =       models.TextField(max_length=1000)
    post_date   =       models.DateTimeField(auto_now_add=True)
    blog        =       models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return self.description
    
  


class Subscribe(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Subscribe"
        verbose_name_plural = "Subscribers"

    def __str__(self):
            return self.email
    


@receiver(post_save, sender=Blog)
def sendMail(sender, **kwargs):
    subject= kwargs['instance'].title
    # currentSite = get_current_site(request)
    # message="http://{d}/{s}".format(d = currentSite.get_host(), s = kwargs['instance'].slug)
    # message='http://{}'.format(Site.objects.get_current().domain)
    message = "http://127.0.0.1:8000/detail/{}".format(kwargs['instance'].slug)
    sender = settings.EMAIL_HOST_USER
    receiver= []
    sub = Subscribe.objects.all()
    for i in sub:
        if i.email not in receiver:
            receiver.append(i.email)
    send_mail( subject, message, sender, receiver)

class BlogReply(models.Model):
    name        =       models.CharField(max_length=100)
    email       =       models.CharField(max_length=100)
    description =       models.TextField(max_length=1000)
    post_date   =       models.DateTimeField(auto_now_add=True)
    comment     =       models.ForeignKey(BlogComment, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return self.name

    
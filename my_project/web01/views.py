from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import ContentForm
from .models import Content
# Create your views here.

def index(request):
    # contents = Content.objects.all()
    return render(request,"web01/index.html")

def listForm(request):
    return render(request,"web01/form.html")

def createList(request):
    new_list = ContentForm(request.POST)
    new_list.save()
    contents = Content.objects.all()
    return render(request,"web01/list.html", {'contents':contents})

def viewList(request):
    contents = Content.objects.all()
    return render(request,"web01/list.html", {'contents':contents})

def moreView(request):
    get_id = request.GET['id']
    content = Content.objects.get(id = get_id)
    content.cnt = cnt+1
    content.save()
    return render(request,'web01/view.html',content)
    # return HttpResponseRedirect(reverse('web01/view.html',id={'id': get_id}))
    # return render(request,"web01/view.html",{'content':content})

    # return HttpResponseRedirect(reverse('moreView'))
    # return HttpResponse(template.render("web01/view.html", get_id))
    # return render(request,"web01/view.html",HttpResponse(content.id))

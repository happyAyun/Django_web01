from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from .forms import ContentForm
from .models import Content, User


# Create your views here.

def index(request):
    # contents = Content.objects.all()
    return render(request,"web01/index.html")

def listForm(request):
    return render(request,"web01/form.html")

def login(request):
    return render(request,"web01/login.html")

def join(request):
    return render(request,"web01/join.html")

def createList(request):
    title = request.POST.get('title',None)
    context = request.POST.get('context',None)
    res_data = {}
    if not (title and context):
        res_data['error']="모든 항목을 입력하세요."
        return render(request,'web01/form.html',res_data)
    else :
        content = Content(
            title=title,
            context=context
        )
        content.save()
        contents = Content.objects.all()
        return render(request,"web01/list.html", {'contents':contents})


def viewList(request):
    contents = Content.objects.all()
    return render(request,"web01/list.html", {'contents':contents})


def moreView(request): 
    get_id = request.GET['id']
    content = Content.objects.get(id = get_id)
    cnt = content.cnt
    content.cnt = cnt + 1
    content.save()
    return render(request,"web01/view.html",{'content':content})

def deleteList(request):
    get_id = request.GET['id']
    content = Content.objects.get(id = get_id)
    content.delete()
    return HttpResponseRedirect(reverse("viewList"))

def updateList(request):
    get_id = request.GET['id']
    content = Content.objects.get(id = get_id)
    return render(request,"web01/update_form.html",{'content':content})

def updateView(request):
    m_id = request.POST['id']
    m_title = request.POST.get('title',None)
    m_context = request.POST.get('context',None)
    res_data = {}
    if not (m_title and m_context):
        res_data['error']="모든 항목을 입력하세요."
        return render(request,'web01/update_form.html',res_data)
    else :
        content = Content.objects.get(id=m_id)
        content.title = m_title
        content.context = m_context
        content.save()
        contents = Content.objects.all()
        return render(request,'web01/list.html',{'contents':contents})

def listSearch(request):
    s_text = request.GET['text']
    if not s_text:
        contents = Content.objects.all()
        return render(request, 'web01/list.html',{'contents' : contents})
    else:
        contents = Content.objects.all().filter(Q(title__icontains=s_text) | Q(context__icontains=s_text)).distinct()
        return render(request,'web01/list.html',{'contents':contents})

        
def userJoin(request):
    get_id = request.POST.get('user_id', None)
    get_pw = request.POST.get('password',None)
    get_pw2 = request.POST.get('password2',None)
    res_data = {}
    if not (get_id and get_pw and get_pw2):
        res_data['error'] = "모든 항목을 입력해주세요."
        return render(request,"web01/join.html",res_data)
    elif get_pw != get_pw2 :
        res_data['pw_error'] = "비밀번호가 서로 다릅니다."
        return render(request,"web01/join.html",res_data)
    else:
        user = User(
            user_id = get_id,
            password = get_pw,
        )
        user.save()
        return HttpResponseRedirect(reverse("login"))
        




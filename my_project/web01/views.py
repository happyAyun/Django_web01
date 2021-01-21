from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from .forms import ContentForm
from .models import Content, User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.
import bcrypt

def index(request):
    return render(request,"web01/index.html")

def listForm(request):
    return render(request,"web01/form.html")

def login(request):
    return render(request,"web01/login.html")

def join(request):
    return render(request,"web01/join.html")

def createList(request):
    if request.session['user']:
        return HttpResponse(request.session['user'])
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
    
    users = User.objects.all()
    for u in users:
        if u.user_id == get_id:
            res_data['error']="이미 존재하는 id입니다."
            return render(request,"web01/join.html",res_data)
       
    if get_pw != get_pw2 :
        res_data['error'] = "비밀번호가 서로 다릅니다."
        return render(request,"web01/join.html",res_data)

    pw = get_pw.encode('utf-8')
    pw_crypt = bcrypt.hashpw(pw, bcrypt.gensalt()) 
    pw_crypt = pw_crypt.decode('utf-8')

    user = User(
        user_id = get_id,
        password = pw_crypt
    )
    user.save()
    return HttpResponseRedirect(reverse("login"))

def userLogin(request):
    get_id = request.POST.get('user_id',None)
    get_pw = request.POST.get('password',None)
    res_data = {}
    if not (get_id and get_pw):
        res_data['error'] = "모든 항목을 입력하여 주십시오."
        return render(request,'web01/login.html', res_data)

    else:
        users = User.objects.all()
        for u in users:
            if u.user_id == get_id:
                user = u
                if bcrypt.checkpw(get_pw.encode('utf-8'), user.password.encode('utf-8')):
                    request.session['user'] = user.user_id
                    return HttpResponseRedirect('/')
                else:
                    res_data['error'] = "비밀번호를 다시 확인해주십시요." 
                    return render(request,'web01/login.html',res_data)
        res_data['error'] = "해당 아이디가 존재하지 않습니다."
        return render(request,'web01/login.html', res_data)


def logout(request):
    if request.session['user']:
        del request.session['user']
    return HttpResponseRedirect('/')


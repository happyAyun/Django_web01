from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from .forms import ContentForm
from .models import Content, User, Reply
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
import bcrypt
# Create your views here.

def index(request):
    return render(request,"web01/index.html")

def listForm(request):
    return render(request,"web01/form.html")

def login(request):
    return render(request,"web01/login.html")

def join(request):
    return render(request,"web01/join.html")

def createList(request):
    if request.session.get('user'):
        u = request.session.get('user')
        title = request.POST.get('title',None)
        context = request.POST.get('context',None)
        res_data = {}
        if not (title and context):
            res_data['error']="모든 항목을 입력하세요."
            return render(request,'web01/form.html',res_data)
        else :
            user = User.objects.get(user_id = u)
            content = Content(
                title=title,
                context=context,
                userId=user
            )
            content.save()
            contents = Content.objects.all()
            page = request.GET.get('page',1)
            paginator = Paginator(contents,5)
            page_obj = paginator.get_page(page)
            return render(request,"web01/list.html", {'contents':page_obj,'user_id':user.user_id})
    else:
        return render(request,'web01/form.html',{'not_login' : True})


def viewList(request):
    contents = Content.objects.all()
    page = request.GET.get('page',1)
    paginator = Paginator(contents,5)
    page_obj = paginator.get_page(page)
    return render(request,"web01/list.html", {'contents':page_obj})

def moreView(request): 
    get_id = request.GET['id']
    if request.session.get('user'):
        get_user = request.session['user']
    else:
        get_user = None
    content = Content.objects.get(id = get_id)
    replies = Reply.objects.filter(originalCon=content)
    content.cnt = content.cnt + 1
    content.save()
    return render(request,"web01/view.html",{'content':content,'replies':replies, 'user':get_user})

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

def createReply(request):
    if request.session.get('user'):
        tid = request.POST.get('id',None)
        context = request.POST.get('context',None)
        content_id = request.POST.get('content.id',None)
        content = Content.objects.get(id = content_id)
        get_user = request.session['user']
        if not context:
            replies = Reply.objects.all().filter(originalCon=content_id)
            return render(request,'web01/view.html',{'not_write':True, 'content':content, 'replies':replies, 'user':get_user})
        if not tid:
            reply = Reply(
                user = get_user,
                replyCon = context,
                originalCon = content
            )
            reply.save()
            replies = Reply.objects.all().filter(originalCon=content_id)
            return render(request,'web01/view.html',{'content':content,'replies':replies,'user':get_user})
        else:
            reply = Reply.objects.get(id=tid)
            reply.replyCon = context
            reply.save()
            replies = Reply.objects.all().filter(originalCon=content_id) 
            return render(request,'web01/view.html',{'content':content,'replies':replies,'user':get_user}) 
    else:
        return render(request,'web01/login.html',{'not_login':True})

def myCreateReply(request):
    tid = request.POST.get('id',None)
    context = request.POST.get('context',None)
    content_id = request.POST.get('content.id',None)
    content = Content.objects.get(id = content_id)
    get_user = request.session['user']
    if not context:
        replies = Reply.objects.all().filter(originalCon=content_id)
        return render(request,'web01/myArticle.html',{'not_write':True, 'content':content, 'replies':replies, 'user':get_user})
    if not tid:
        reply = Reply(
            user = get_user,
            replyCon = context,
            originalCon = content
        )
        reply.save()
        replies = Reply.objects.all().filter(originalCon=content_id)
        return render(request,'web01/myArticle.html',{'content':content,'replies':replies,'user':get_user})
    else:
        reply = Reply.objects.get(id=tid)
        reply.replyCon = context
        reply.save()
        replies = Reply.objects.all().filter(originalCon=content_id) 
        return render(request,'web01/myArticle.html',{'content':content,'replies':replies,'user':get_user}) 

def deleteReply(request):
    get_id = request.GET['id']
    get_cId = request.GET['c_id']
    reply = Reply.objects.get(id = get_id)
    reply.delete()
    replies = Reply.objects.all()
    content = Content.objects.get(id = get_cId)
    if request.session.get('user'):
        get_user = request.session.get('user')
    return render(request,'web01/view.html',{'content':content, 'replies':replies, 'user':get_user})

def myDeleteReply(request):
    get_id = request.POST.get('id',None)
    get_cId = request.POST.get('c_id',None)
    reply = Reply.objects.get(id = get_id)
    reply.delete()
    replies = Reply.objects.all()
    content = Content.objects.get(id = get_cId)
    if request.session.get('user'):
        get_user = request.session.get('user')
    return render(request,'web01/myArticle.html',{'content':content, 'replies':replies, 'user':get_user})

def myPage(request):
    return render(request, 'web01/myPage.html')

def pwChange(request):
    return render(request, 'web01/pwChange.html')

def changePW(request):
    pw = request.POST.get('password',None)
    pw1 = request.POST.get('re_pw',None)
    pw2 = request.POST.get('re_pw2',None)
    res_data={}
    if not (pw and pw1 and pw2):
        res_data['error'] = '모든 항목을 입력하여 주십시요.'
        return render(request, 'web01/pwChange.html',res_data)
    
    user = request.session['user']
    user = User.objects.get(user_id = user)
    if bcrypt.checkpw(pw.encode('utf-8'), user.password.encode('utf-8')):
        if pw1 != pw2:
            res_data['error'] = '변경할 비밀번호 입력이 서로 다릅니다.'
            return render(request, 'web01/pwChange.html',res_data)
        else:
            pw1 = pw1.encode('utf-8')
            pw1 = bcrypt.hashpw(pw1, bcrypt.gensalt())
            pw1 = pw1.decode('utf-8')
            user.password = pw1
            user.save()
            return render(request, 'web01/myPage.html', {'pw_change':True})

    else:
        res_data['error'] = '현재의 비밀번호가 일치하지 않습니다.'
        return render(request, 'web01/pwChange.html',res_data)

def secession(request):
    return render(request,'web01/secession.html')

def myWriting(request):
    user = request.session['user']
    user = User.objects.get(user_id=user)
    contents = Content.objects.all().filter(userId=user)
    page = request.GET.get('page',1)
    paginator = Paginator(contents,5)
    page_obj = paginator.get_page(page)
    return render(request, 'web01/myWriting.html', {'contents':page_obj})

def resetUser(request):
    pw = request.POST.get('password',None)
    res_data = {}
    if not pw:
        res_data['error'] = '비밀번호를 입력하여 주세요.'
        return render(request,'web01/secession.html',res_data)

    user = request.session['user']
    user = User.objects.get(user_id=user)
    if bcrypt.checkpw(pw.encode('utf-8'), user.password.encode('utf-8')):
        user.delete()
        del request.session['user']
        return render(request,'web01/index.html',{'reset':True})

    else:
        res_data['error'] = '비밀번호가 일치하지 않습니다.'
        return render(request,'web01/secession.html', res_data)

def myArticle(request):
    get_id = request.GET['id']
    content = Content.objects.get(id = get_id)
    replies = Reply.objects.filter(originalCon=content)
    get_user = request.session['user']
    return render(request,"web01/myArticle.html",{'content':content,'replies':replies, 'user':get_user})

# def modifyReply(request):
#     re_id = request.POST.get('id',None)
#     con_id = request.POST.get('c_id',None)
#     re_context = request.POST.get('context',None)
#     reply = Reply.objects.get(id = re_id)
#     content = Content.objects.get(id = con_id)
#     get_user = request.session['user']
#     if not re_context:
#         replies = Reply.objects.filter(originalCon=content)
#         return render(request,"web01/view.html",{'content':content,'replies':replies, 'user':get_user,'not_change':True})
#     reply.replyCon = re_context
#     reply.save()
#     replies = Reply.objects.filter(originalCon=content)
#     return render(request,'web01/view.html',{'content':content,'replies':replies, 'user':get_user})

    
    
    

    
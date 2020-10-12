from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
import json
from django.core import serializers
from django.core.paginator import Paginator
from django.forms import model_to_dict
import requests
import re
import time
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import loader, Context
from django.db.models import Q
import datetime
# Create your views here.

def vlogLetter(request):                #主页
    return render(request, 'home.html', {})


def vlogList(request):                  #博客列表
    # 获取天气信息
    # 获取ip所在区域
    try:
        headers = {
            "Host": "www.sojson.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"
        }
        url = "https://www.sojson.com/ip/"
        req = requests.get(url, headers=headers)
        a = req.text.find("腾讯定位")
        b = req.text.find("<td>", a)
        a = req.text.find("</td>", b)
        id_addr = re.search("[\u4e00-\u9fa5]+", req.text[b:a])
        id_addr = id_addr.group()
        place = re.split("省|自治区|市|区", id_addr)
        area = place[2]
        # 获取区域编码
        headers = {
            "Host": "toy1.weather.com.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"
        }
        url = "http://toy1.weather.com.cn/search?cityname=" + area
        req = requests.get(url, headers=headers)
        place = re.search("[0-9]+", req.text)
        code = place.group()
        #天气信息
        headers = {
            "Host": "d1.weather.com.cn",
            "Referer": "http://www.weather.com.cn/weather1d/" + code + ".shtml",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"
        }
        url = "http://d1.weather.com.cn/sk_2d/" + code + ".html?_=" + str(int(time.time() * 1000))
        req = requests.get(url, headers=headers)
        req.encoding = req.apparent_encoding
        Info = re.search("{.*}", req.text).group()
        Info = json.loads(Info)
    except:
        Info = {"error": "获取失败"}
        id_addr = "获取地址失败"
    #分页
    number = []
    blog = vlogText.objects.all().order_by("-id")
    bgt = VlogType.objects.all()
    for type in bgt.order_by("-id"):
        number.append(blog.filter(blog_type=type).count())
    number.append(blog.count())
    paginator = Paginator(blog, 5)
    pindex = request.GET.get('page', 1)             #路由单纯传参，不做路径
    page = Paginator.page(paginator, pindex)
    content = {'bgt': bgt, 'page': page, 'number': number, 'Place': id_addr, 'W_Info': Info}  #'Place': id_addr.group(),
    return render(request, 'vlogList.html', content)

def vgpage(request):                  #博客分页
    blog = vlogText.objects.all().order_by("-id")
    paginator = Paginator(blog, 5)
    pindex = request.GET.get('page', 1)             #路由单纯传参，不做路径
    page = Paginator.page(paginator, pindex)
 #   jsonstr = model_to_dict(page)
    bg_page = serializers.serialize("json", page.object_list, ensure_ascii=False, use_natural_foreign_keys=True)
    cnt = {'bg_page': bg_page, 'number': page.paginator.num_pages}
    content = json.dumps(cnt, ensure_ascii=False)
    return HttpResponse(content, content_type="application/json", charset='utf-8')


#  jquery ajax
def vgS(request, id):                       #类型
    bgt = VlogType.objects.get(id=id)
    blog = vlogText.objects.filter(blog_type=bgt).order_by("-id")
    paginator = Paginator(blog, 5)
    pindex = request.GET.get('page', 1)  # 路由单纯传参，不做路径
    page = Paginator.page(paginator, pindex)
    content = {'bgt': bgt, 'page': page}
    return render(request, 'vlogSort.html', content)

def vgsort(request,id):                     #分类分页
    bgt = VlogType.objects.get(id=id)
    blog = vlogText.objects.filter(blog_type=bgt).order_by("-id")
    paginator = Paginator(blog, 5)
    pindex = request.GET.get('page', 1)  # 路由单纯传参，不做路径
    page = Paginator.page(paginator, pindex)
    bg_page = serializers.serialize("json", page.object_list, ensure_ascii=False, use_natural_foreign_keys=True)
    cnt = {'bg_page': bg_page, 'number': page.paginator.num_pages}
    content = json.dumps(cnt, ensure_ascii=False)
    return HttpResponse(content, content_type="application/json", charset='utf-8')


def login(request):             #登录
    if request.method == "GET":
        return render(request, 'login.html', {})
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        syn = request.POST.get("syn", 0)
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            if syn == 0:
               return redirect('/')
            else:
                return HttpResponse(json.dumps({"success": "成功登录"}, ensure_ascii=False))
        else:
            return render(request, 'login.html', {"user": user, "error": "密码或者帐号错误，请输入正确密码或账号！"})

def register(request):          #注册
    if request.method == "GET":
        return render(request, 'register.html', {})
    if request.method == "POST":
        username = request.POST.get('username')
        psw = request.POST.get('pwd')
        pswconfirm = request.POST.get('pwdconfirm')
        mail = request.POST.get('mail')
        user = User.objects.get(username=username)
        if user:
            return render(request, 'register.html', {"error": "用户名已存在"})
        if psw != pswconfirm:
            return render(request, 'register.html', {"error": "两次输入密码不一致"})

        title = '用户激活邮件'
        message = loader.get_template('email.html')
        msg = message.render({"user": username})
        from_mail = '1171575420@qq.com'
        send_mail(title, '', from_mail, [mail], html_message=msg)

        User.objects.create_user(is_active=False, is_staff=False, username=username, password=psw, email=mail)
        return redirect('/login/')

def verify(request):
    username = request.GET.get("user")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    if user is not None:
        user.is_active = True
        user.save()
        return HttpResponse(json.dumps({"success": "成功激活"}, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({"error": "激活失败"}, ensure_ascii=False))

def logout(request):                    #退出登录
    if request.method == 'GET':
        auth.logout(request)
    return redirect("/")


def vgcontent(request):   #博客具体内容
    id = request.GET.get("id")
    blog = vlogText.objects.get(id=id)
    root_comment = comment.objects.filter(belond=blog, parent=None).order_by("-id")
    content = {'blog': blog, "root_comment": root_comment}
    return render(request, 'vlog_content.html', content)

def Comment(request):
    comt = request.POST.get("comment")
    blog_id = request.POST.get("id")
    blog = vlogText.objects.get(id=blog_id)
    username = request.user.username
    user = User.objects.get(username=username)
    parent_id = request.POST.get("parent", None)
    if parent_id:
        parent = comment.objects.get(id=parent_id)
    else:
        parent = None
    root_id = request.POST.get("root", None)
    if root_id:
        root = comment.objects.get(id=root_id)
    else:
        root = None
    if comt != "":
        try:
            cmt = comment()
            cmt.comt = comt
            cmt.belond = blog
            cmt.user = user
            cmt.root = root
            cmt.parent = parent
            cmt.save()
        except:
            return HttpResponse(json.dumps({"success": "提交评论失败", "state": 100}, ensure_ascii=False))
        if parent:
            reply_to = parent.user.username
        else:
            reply_to = "author"
        if root_id:
            rt_id = root_id
        else:
            rt_id = cmt.id
        return HttpResponse(json.dumps({"success": "提交评论成功", "com_id": cmt.id, "root_id": rt_id, "reply_to": reply_to}, ensure_ascii=False))
    else:
        return HttpResponse(json.dumps({"error": "提交评论失败", "state": 101}, ensure_ascii=False))


def search(request):                            #搜索
    word = request.POST.get("word")
    if word:
        search_result = vlogText.objects.filter(Q(title__icontains=word) | Q(content__icontains=word))
        content = {"search_result": search_result, "word": word}
        return render(request, 'search_result.html', content)
    else:
        return render(request, 'search_result.html')


def sign_in(request):
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    day = today.day
    username = request.user.username
    user = User.objects.get(username=username)
    sign = geton.objects.filter(time__year=year, time__month=month, time__day=day, user=user)
    if sign:
        return HttpResponse(json.dumps({"success": "已签到", "state": 100}, ensure_ascii=False))
    else:
        try:
            sign = geton()
            sign.user = user
            sign.Is_sign = True
            sign.save()
            return HttpResponse(json.dumps({"success": "成功签到", "state": 100}, ensure_ascii=False))
        except:
            return HttpResponse(json.dumps({"fail": "签到失败", "state": 10021}, ensure_ascii=False))

def person(request):  # 个人页
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    day = today.day
    username = request.user.username
    user = User.objects.get(username=username)
    sign = geton.objects.filter(time__year=year, time__month=month, time__day=day, user=user)
    if sign:
        Is_sign = True
    else:
        Is_sign = False
    return render(request, 'person.html', {"Is_sign": Is_sign})

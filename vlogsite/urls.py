from django.conf.urls import include
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.vlogLetter, name='home'),      #首页
    path('vgList/', views.vlogList, name='vgList'),   #博客列表
    path('vgpage/', views.vgpage, name='vgpage'),       #分页
    path('vgS/<int:id>', views.vgS, name='vgS'),
    path('vgsort/<int:id>', views.vgsort, name='vgsort'),        #博客分类
    path('vgcontent/', views.vgcontent, name='vgct'),     #博客详细内容
    path('login/', views.login, name='login'),            #登录
    path('register/', views.register, name='register'),    #注册
    path('verify/', views.verify, name='verify'),       #验证
    path('logout/', views.logout, name='logout'),       #退出登录
    path('personal', login_required(views.person), name='person'),   #个人页
    path('Comment/', login_required(views.Comment), name='Comment'),  #发表评论
    path('search/', views.search, name='search'),           #查询
    path('sign_in/', login_required(views.sign_in), name="sign"),           #签到
]
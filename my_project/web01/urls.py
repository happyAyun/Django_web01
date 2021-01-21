
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('',views.index,name="index"),

    re_path(r'/createList/$', views.createList, name="createList"),

    re_path(r'/listForm/$', views.listForm, name="listForm"),

    re_path(r'/viewList/$', views.viewList, name="viewList"),

    re_path(r'/moreView/$', views.moreView, name="moreview"),

    re_path(r'/deleteList/$', views.deleteList, name="deleteList"),

    re_path(r'/updateList/$', views.updateList, name="updateList"),

    re_path(r'/updateView/$', views.updateView, name="updateView"),

    re_path(r'/listSearch/$', views.listSearch, name="listSearch"),

    re_path(r'/join/$', views.join, name="join"),

    re_path(r'/login/$', views.login, name="login"),

    re_path(r'/userJoin/$', views.userJoin, name="userJoin"),

    re_path(r'/userLogin/$', views.userLogin, name="userLogin"),

    re_path(r'/logout/$', views.logout, name="logout"),
]
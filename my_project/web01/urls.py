
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('',views.index,name="index"),

    path('listForm/createList/', views.createList, name="createList"),
    re_path(r'/createList/$', views.createList, name="createList"),

    path('listForm/', views.listForm, name="listForm"),
    re_path(r'/listForm/$', views.listForm, name="listForm"),

    path('viewList/', views.viewList, name="viewList"),
    re_path(r'/viewList/$', views.viewList, name="viewList"),

    path('viewList/moreView/', views.moreView, name="moreView"),
    re_path(r'/moreView/$', views.moreView, name="moreview"),

    path('viewList/moreView/deleteList/', views.deleteList, name="deleteList"),
    re_path(r'/deleteList/$', views.deleteList, name="deleteList"),

    path('viewList/moreView/updateList/', views.updateList, name="updateList"),
    re_path(r'/updateList/$', views.updateList, name="updateList"),

    path('viewList/moreView/updateList/updateView/', views.updateView, name="updateView"),
    re_path(r'/updateView/$', views.updateView, name="updateView"),

    path('viewList/listSearch', views.listSearch, name="listSearch"),
    re_path(r'/listSearch/$', views.listSearch, name="listSearch"),

    path('join/', views.join, name="join"),
    re_path(r'/join/$', views.join, name="join"),

    path('login/', views.login, name="login"),
    re_path(r'/login/$', views.login, name="login"),

    path('userJoin/', views.userJoin, name="userJoin"),
    re_path(r'/userJoin/$', views.userJoin, name="userJoin"),

    # path('')
]

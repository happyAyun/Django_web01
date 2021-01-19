
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('listForm/createList/', views.createList, name="createList"),
    path('listForm/', views.listForm, name="listForm"),
    path('viewList/', views.viewList, name="viewList"),
    path('viewList/moreView/', views.moreView, name="moreView"),
    
    # path('viewList/', views.list_view, name="viewList"),
]

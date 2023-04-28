from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    CustomLoginView, RegisterPage,
    TaskList, TaskDetail, TaskCreate, 
    TaskUpdate, TaskDelete,
)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('create/', TaskCreate.as_view(), name='task-create'),
    path('<int:pk>/edit', TaskUpdate.as_view(), name='task-update'),
    path('<int:pk>/delete', TaskDelete.as_view(), name='task-delete'),
]

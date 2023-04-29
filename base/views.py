from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView
)

from .models import Task


class PreventUnauthorizedMixin(object):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])

        if task.user != request.user:
            raise Http404

        return super().get(request, *args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # User tasks
        user_tasks = context['tasks'].filter(user=self.request.user)
        context['tasks'] = user_tasks
        context['count'] = user_tasks.filter(is_completed=False).count()

        # Searching
        if search_input := self.request.GET.get('search', ''):
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search'] = search_input
        
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'

    def get_queryset(self):
        # Prevent user to see items from other users
        return Task.objects.filter(user=self.request.user)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'is_completed']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(PreventUnauthorizedMixin, LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'is_completed']
    success_url = reverse_lazy('task-list')


class TaskDelete(PreventUnauthorizedMixin, LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')


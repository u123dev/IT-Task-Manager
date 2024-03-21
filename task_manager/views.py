from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import (
    PositionSearchForm,
    TaskTypeSearchForm,
    WorkerSearchForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    TaskCreationForm,
    TaskSearchForm,
    WorkerFilterForm
)
from task_manager.models import Task, Worker, Position, TaskType


def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    num_tasks = Task.objects.count()
    num_tasks_in_progress = Task.objects.filter(is_completed=False).count()
    num_workers = Worker.objects.count()
    num_positions = Position.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "num_tasks_in_progress": num_tasks_in_progress,
        "num_positions": num_positions,
        "num_visits": num_visits + 1,
        "segment" : "dashboard",    # for template

    }

    return render(request, "task_manager/index.html", context=context)


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "task_manager/position_list.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = Position.objects.all()
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(initial={"name": name})
        context["segment"] = "position_list"    # for template
        return context


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "tasktype_list"
    template_name = "task_manager/tasktype_list.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(initial={"name": name})
        context["segment"] = "tasktype_list"    # for template
        return context


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tasktype-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tasktype-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:tasktype-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 3

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        context["segment"] = "worker_list"    # for template
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("tasks")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        is_completed = self.request.GET.get("is_completed", "")
        context["filter_form"] = WorkerFilterForm(
            initial={"is_completed": is_completed}
        )

        worker = self.object
        tasks = Task.objects.filter(assignees=worker)
        if is_completed == "no":
            tasks = tasks.filter(is_completed=False)
        elif is_completed == "yes":
            tasks = tasks.filter(is_completed=True)

        context["tasks"] = tasks

        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 3

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        context["segment"] = "task_list"    # for template
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.all().prefetch_related("assignees")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreationForm


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreationForm


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskAssignWorker(LoginRequiredMixin, generic.DetailView):
    model = Task

    def post(self, request, **kwargs):
        self.object = self.get_object()
        worker = Worker.objects.get(id=request.user.id)
        pk = self.kwargs.get("pk")
        if self.object in worker.tasks.all():
            worker.tasks.remove(pk)
        else:
            worker.tasks.add(pk)
        return HttpResponseRedirect(self.object.get_absolute_url())


class TaskSetCompleted(LoginRequiredMixin, generic.DetailView):
    model = Task

    def post(self, request, **kwargs):
        self.object = self.get_object()
        self.object.is_completed = not self.object.is_completed
        self.object.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


def about(request: HttpRequest) -> HttpResponse:
    """View function for the about page of the site."""

    context = {
        "segment" : "about",    # for template
    }
    return render(request, "task_manager/about.html", context=context)

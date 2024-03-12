from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from task_manager.models import Task, Worker, Position


def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()
    num_positions = Position.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "num_positions": num_positions,
        "num_visits": num_visits + 1,
    }

    return render(request, "task_manager/index.html", context=context)

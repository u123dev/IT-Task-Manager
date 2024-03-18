from django.urls import path

from task_manager.views import (
    index,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerDeleteView,
    WorkerUpdateView,
    TaskListView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    TaskCreateView,
    TaskSetCompleted,
    TaskAssignWorker,
    about
)

urlpatterns = [
    path("", index, name="index"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("tasktypes/", TaskTypeListView.as_view(), name="tasktype-list"),
    path("tasktypes/create/", TaskTypeCreateView.as_view(), name="tasktype-create"),
    path("tasktypes/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="tasktype-update"),
    path("tasktypes/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="tasktype-delete"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/toggle-assign/", TaskAssignWorker.as_view(), name="toggle-task-assign"),
    path("tasks/<int:pk>/set-completed/", TaskSetCompleted.as_view(), name="set-task-completed"),
    path("about/", about, name="about"),
]

app_name = "task_manager"

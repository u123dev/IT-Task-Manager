from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from task_manager.models import Position, TaskType, Task, Worker


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = ("position",) + UserAdmin.list_display
    fieldsets = (
        (("Position", {"fields": ("position",)}),)
    ) + UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                        "email",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "is_completed",
                    "priority", "task_type", "description",
                    )
    search_fields = ("name",)
    list_filter = ("deadline", "is_completed", "priority", "task_type__name",)


admin.site.register(Position)
admin.site.register(TaskType)

admin.site.unregister(Group)

import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from task_manager.models import Worker, Task


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "search position"})
    )


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "search task type"})
    )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "search worker by username"}
        )
    )


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
            "email",
        )


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = (
            "username",
            "first_name",
            "last_name",
            "position",
            "email",
        )


class TaskCreationForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    expected_deadline_date = datetime.date.today() + datetime.timedelta(days=5)
    deadline = forms.DateField(
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
        initial=expected_deadline_date,
    )

    TRUE_FALSE_CHOICES = ((False, "No"), (True, "Yes"))
    is_completed = forms.ChoiceField(
        choices=TRUE_FALSE_CHOICES,
        label="Is Completed ?",
        initial="",
        widget=forms.Select(), required=True)

    class Meta:
        model = Task
        fields = "__all__"

    def clean_deadline(self):
        return validate_deadline(self.cleaned_data["deadline"])


def validate_deadline(deadline):
    if deadline < datetime.date.today():
        raise ValidationError(
            f"Deadline date should be not less than today: "
            f"{datetime.date.today().strftime("%d-%m-%Y")}"
        )

    return deadline


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "search task by name"})
    )

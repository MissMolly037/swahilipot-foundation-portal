from django.contrib import admin

from .models import Task, TaskAttachment, TaskComment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "assigned_to",
        "assigned_by",
        "priority",
        "status",
        "due_date",
    )

    list_filter = (
        "priority",
        "status",
    )

    search_fields = (
        "title",
        "description",
    )

    ordering = (
        "status",
        "due_date",
    )

    autocomplete_fields = (
        "assigned_to",
        "assigned_by",
    )


@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "uploaded_by",
        "uploaded_at",
    )

    autocomplete_fields = (
        "task",
        "uploaded_by",
    )


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "author",
        "progress_update",
        "created_at",
    )

    autocomplete_fields = (
        "task",
        "author",
    )
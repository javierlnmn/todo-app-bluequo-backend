from django.contrib import admin
from .models import Todo, Comment



class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ("created_at",)
    fields = ("user", "content", "created_at")

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "due_date", "user", "assigned_to", "created_at")
    list_filter = ("status", "due_date", "user")
    search_fields = ("title", "description", "user__username", "assigned_to__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ('Todo Details', {
            'fields': ('title', 'description', 'status', 'due_date', 'user', 'assigned_to')
        }),
    )

    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "todo", "created_at")
    search_fields = ("user__username", "todo__title", "content")
    ordering = ("-created_at",)

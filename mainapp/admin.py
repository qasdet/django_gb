from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from mainapp import models as mainapp_models


@admin.register(mainapp_models.News)
class NewsAdmin(admin.ModelAdmin):
    def delete(self, request, queryset):
        for item in queryset:
            item.delete()

    def restore(self, request, queryset):
        for item in queryset:
            item.restore()

    delete.short_description = _("Mark deleted")
    restore.short_description = _("Restore")
    actions = ["delete", "restore"]
    list_display = ["id", "title", "preambule", "body_as_markdown", "created", "updated", "deleted"]
    list_filter = ["created", "deleted"]
    ordering = ["-created"]
    list_per_page = 10


@admin.register(mainapp_models.Lessons)
class LessonsAdmin(admin.ModelAdmin):
    def delete(self, request, queryset):
        for item in queryset:
            item.delete()

    def restore(self, request, queryset):
        for item in queryset:
            item.restore()

    def get_course_name(self, obj):
        return obj.course.name

    delete.short_description = _("Mark deleted")
    restore.short_description = _("Restore")
    get_course_name.short_description = _("Course")
    actions = ["delete", "restore"]
    list_display = ["id", "get_course_name", "num", "title", "description_as_markdown", "created", "updated", "deleted"]
    list_filter = ["description_as_markdown", "created", "deleted"]
    ordering = ["-course__name", "-num"]
    list_per_page = 10


@admin.register(mainapp_models.Courses)
class CoursesAdmin(admin.ModelAdmin):
    def delete(self, request, queryset):
        for item in queryset:
            item.delete()

    def restore(self, request, queryset):
        for item in queryset:
            item.restore()

    delete.short_description = _("Mark deleted")
    restore.short_description = _("Restore")
    actions = ["delete", "restore"]
    list_display = ["id", "name", "created", "cost", "cover", "description_as_markdown", "updated", "deleted"]
    list_filter = ["cost", "description_as_markdown", "created", "deleted"]
    ordering = ["-created"]
    list_per_page = 10


@admin.register(mainapp_models.CourseFeedback)
class CourseFeedbackAdmin(admin.ModelAdmin):
    def delete(self, request, queryset):
        for item in queryset:
            item.delete()

    def restore(self, request, queryset):
        for item in queryset:
            item.restore()

    delete.short_description = _("Mark deleted")
    restore.short_description = _("Restore")
    actions = ["delete", "restore"]
    list_display = ["id", "course", "user", "feedback", "rating", "created", "updated", "deleted"]
    list_filter = ["course", "user", "feedback", "rating", "created", "deleted"]
    ordering = ["-created"]
    list_per_page = 10


@admin.register(mainapp_models.Teachers)
class TeachersAdmin(admin.ModelAdmin):
    def delete(self, request, queryset):
        for item in queryset:
            item.delete()

    def restore(self, request, queryset):
        for item in queryset:
            item.restore()

    delete.short_description = _("Mark deleted")
    restore.short_description = _("Restore")
    actions = ["delete", "restore"]
    list_display = ["id", "name_first", "name_second", "day_birth", "created", "updated", "deleted"]
    list_filter = ["created", "deleted"]
    ordering = ["-created"]
    list_per_page = 10

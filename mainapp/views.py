import logging
from datetime import date
from typing import Any, Dict, Optional

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.http import FileResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
    View,
)

from mainapp import forms as mainapp_forms
from mainapp import models as mainapp_models
from mainapp import tasks as mainapp_tasks

logger = logging.getLogger(__name__)


class MainPageView(TemplateView):
    template_name: str = "mainapp/index.html"


# TODO: починить фильтрацию.
# Не удалось решить проблему с пагинацией при фильтрации новостей в рамках одной вьюхи. При переключении страницы
# фильтры сбрасываются. Костыль в виде сохранения стейта внутри вьюхи (self.date_from, self.date_to) не решил проблему.
class NewsListView(ListView):
    model = mainapp_models.News
    paginate_by = 5
    date_from = ""
    date_to = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "form_data": {
                    "dateFrom": self.date_from,
                    "dateTo": self.date_to,
                }
            }
        )
        return context

    def get_queryset(self):
        query_set = super().get_queryset().filter(deleted=False)
        if self.date_from and self.date_to:
            query_set = query_set.filter(
                created__gt=date.fromisoformat(self.date_from),
                created__lt=date.fromisoformat(self.date_to),
            )
        elif self.date_from:
            query_set = query_set.filter(created__gte=date.fromisoformat(self.date_from))
        elif self.date_to:
            query_set = query_set.filter(created__lte=date.fromisoformat(self.date_to))
        return query_set

    def get(self, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        self.date_from = self.request.POST.get("dateFrom", "")
        self.date_to = self.request.POST.get("dateTo", "")
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = mainapp_models.News
    fields = "__all__"
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.add_news",)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = mainapp_models.News
    fields = "__all__"
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.change_news",)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = mainapp_models.News
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.delete_news",)


class NewsDetailView(DetailView):
    model = mainapp_models.News


class CoursesListView(TemplateView):
    template_name: str = "mainapp/courses.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super(CoursesListView, self).get_context_data(**kwargs)
        context["objects"] = mainapp_models.Courses.objects.all()[:7]
        return context


class CoursesDetailView(TemplateView):
    template_name: str = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs) -> Dict[str, Any]:
        logger.debug("Yet another log message")
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(mainapp_models.Courses, pk=pk)
        context["lessons"] = mainapp_models.Lessons.objects.filter(course=context["course_object"])
        context["teachers"] = mainapp_models.Teachers.objects.filter(course=context["course_object"])
        if not self.request.user.is_anonymous:
            if not mainapp_models.CourseFeedback.objects.filter(
                course=context["course_object"], user=self.request.user
            ).count():
                context["feedback_form"] = mainapp_forms.CourseFeedbackForm(
                    course=context["course_object"], user=self.request.user
                )

        cached_feedback = cache.get(f"feedback_list_{pk}")
        if not cached_feedback:
            context["feedback_list"] = (
                mainapp_models.CourseFeedback.objects.filter(course=context["course_object"])
                .order_by("-created", "-rating")[:5]
                .select_related()
            )
            cache.set(f"feedback_list_{pk}", context["feedback_list"], timeout=300)  # 5 minutes

            # Archive object for tests --->
            # import pickle

            # with open(f"mainapp/fixtures/005_feedback_list_{pk}.bin", "wb") as outf:
            #     pickle.dump(context["feedback_list"], outf)
            # <--- Archive object for tests

        else:
            context["feedback_list"] = cached_feedback

        return context


class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = mainapp_models.CourseFeedback
    form_class = mainapp_forms.CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string("mainapp/includes/feedback_card.html", context={"item": self.object})
        return JsonResponse({"card": rendered_card})


class ContactsPageView(TemplateView):
    template_name: str = "mainapp/contacts.html"

    def get_context_data(self, **kwargs: any) -> Dict[str, Any]:
        context = super(ContactsPageView, self).get_context_data(**kwargs)
        context["data"] = mainapp_models.contacts_data
        if self.request.user.is_authenticated:
            context["form"] = mainapp_forms.MailFeedbackForm(user=self.request.user)
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(f"mail_feedback_lock_{self.request.user.pk}")
            if not cache_lock_flag:
                cache.set(
                    f"mail_feedback_lock_{self.request.user.pk}",
                    "lock",
                    timeout=300,
                )
                messages.add_message(self.request, messages.INFO, _("Message sended"))
                mainapp_tasks.send_feedback_mail.delay(
                    {
                        "user_id": self.request.POST.get("user_id"),
                        "message": self.request.POST.get("message"),
                    }
                )
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    _("You can send only one message per 5 minutes"),
                )
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


class DocSitePageView(TemplateView):
    template_name: str = "mainapp/doc_site.html"


class GoogleRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs) -> Optional[str]:
        domain = "https://www.google.com"
        param = self.request.GET["param"]
        self.url = f"{domain}/search?q={param}"
        return super().get_redirect_url(*args, **kwargs)


class LogView(TemplateView):
    template_name = "mainapp/log_view.html"

    def get_context_data(self, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        if settings.LOG_FILE.exists:
            with open(settings.LOG_FILE, "r") as log_file:
                for i, line in enumerate(log_file):
                    if i == 1000:  # first 1000 lines
                        break
                    log_slice.insert(0, line)  # append at start
        context["log"] = "".join(log_slice)
        return context


class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))

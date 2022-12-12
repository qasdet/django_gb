from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic import RedirectView

from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

# Время 0 в режиме debug необходимо, чтобы нормально работали crud-тесты selenium
if settings.DEBUG:
    cache_time = 60 * 5  # 5 minutes
else:
    cache_time = 0

# TODO: починить кэш новостей.
# Кэш для News пришлось убрать, так как состояние новостей кэшируются вместе с контролами при первом посещении станицы
# и не обновляется после смены статуса пользователя (авторизован/не авторизован).

if settings.DEBUG:
    cache_time = 60 * 5  # 5 minutes
else:
    cache_time = 0


urlpatterns = [
    path("", RedirectView.as_view(url="index")),
    path("index", views.MainPageView.as_view(), name="index"),
    path("news/", views.NewsListView.as_view(), name="news"),
    path("news/create/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/<int:pk>/detail", cache_page(cache_time)(views.NewsDetailView.as_view()), name="news_detail"),
    path("news/<int:pk>/update", views.NewsUpdateView.as_view(), name="news_update"),
    path("news/<int:pk>/delete", views.NewsDeleteView.as_view(), name="news_delete"),
    path("courses/", cache_page(cache_time)(views.CoursesListView.as_view()), name="courses"),
    path("courses/<int:pk>/", cache_page(cache_time)(views.CoursesDetailView.as_view()), name="courses_detail"),
    path("course_feedback/", views.CourseFeedbackFormProcessView.as_view(), name="course_feedback"),
    path("contacts/", cache_page(cache_time)(views.ContactsPageView.as_view()), name="contacts"),
    path("doc_site/", cache_page(cache_time)(views.DocSitePageView.as_view()), name="doc_site"),
    path("search-in-google", views.GoogleRedirectView.as_view(), name="search_in_google"),
    path("log_view/", views.LogView.as_view(), name="log_view"),
    path("log_download/", views.LogDownloadView.as_view(), name="log_download"),
]

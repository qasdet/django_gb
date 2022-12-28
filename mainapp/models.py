import json

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class MainappModelManager(models.Manager):
    # def get_queryset(self):
    #     return super().get_queryset().filter(deleted=False)
    pass


class MainappBaseModel(models.Model):
    objects = MainappModelManager()

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"), editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated"), editable=False)
    deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))

    def delete(self, *args):
        self.deleted = True
        self.save()

    def restore(self, *args):
        self.deleted = False
        self.save()

    class Meta:
        abstract = True


class News(MainappBaseModel):
    title = models.CharField(max_length=256, verbose_name=_("Title"))
    preambule = models.CharField(max_length=1024, verbose_name=_("Preambule"))
    body = models.TextField(blank=True, null=True, verbose_name=_("Body"))
    body_as_markdown = models.BooleanField(default=False, verbose_name=_("As markdown"))

    def __str__(self) -> str:
        return f"{self.pk} {self.title}"

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ("-created",)


class Courses(MainappBaseModel):
    name = models.CharField(max_length=256, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    description_as_markdown = models.BooleanField(default=False, verbose_name=_("As markdown"))
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name=_("Cost"))
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name=_("Cover"))

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")


class CourseFeedback(MainappBaseModel):
    RATING = ((5, "⭐⭐⭐⭐⭐"), (4, "⭐⭐⭐⭐"), (3, "⭐⭐⭐"), (2, "⭐⭐"), (1, "⭐"))
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name=_("Course"))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("User"))
    feedback = models.TextField(default=_("No feedback"), verbose_name=_("Feedback"))
    rating = models.SmallIntegerField(choices=RATING, default=5, verbose_name=_("Rating"))

    def __str__(self):
        return f"{self.course} ({self.user})"


class Lessons(MainappBaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name=_("Lesson number"))
    title = models.CharField(max_length=256, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    description_as_markdown = models.BooleanField(default=False, verbose_name=_("As markdown"))

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        ordering = ("course", "num")
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")


class Teachers(MainappBaseModel):
    course = models.ManyToManyField(Courses)
    name_first = models.CharField(max_length=128, verbose_name="Name")
    name_second = models.CharField(max_length=128, verbose_name="Surname")
    day_birth = models.DateField(default=False)

    def __str__(self) -> str:
        return f"{self.pk:0>3} {self.name_second} {self.name_first}"

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")


contacts_data = json.loads(
    """
[
  {
    "links": [
      {
        "name": "Петропавловская крепость",
        "href": "https://yandex.ru/maps/org/petropavlovskaya_krepost/146720535721/?utm_medium=mapframe&utm_source=maps"
      },
      {
        "name": "Достопримечательность в Санкт‑Петербурге",
        "href": "https://yandex.ru/maps/2/saint-petersburg/category/landmark_attraction/89683368508/?utm_medium=mapframe&utm_source=maps"
      },
      {
        "name": "Музей в Санкт‑Петербурге",
        "href": "https://yandex.ru/maps/2/saint-petersburg/category/museum/184105894/?utm_medium=mapframe&utm_source=maps"
      }
    ],
    "frame_link": "https://yandex.ru/map-widget/v1/-/CCUAZHcrhA",
    "title": "Санкт‑Петербург",
    "phone": "+7-999-11-11111",
    "email": "geeklab@spb.ru",
    "address": "территория Петропавловская крепость, 3Ж"
  },
  {
    "links": [
      {
        "name": "Казанский Кремль",
        "href": "https://yandex.ru/maps/org/kazanskiy_kreml/95813866834/?utm_medium=mapframe&utm_source=maps"
      },
      {
        "name": "Музей в Казани",
        "href": "https://yandex.ru/maps/43/kazan/category/museum/184105894/?utm_medium=mapframe&utm_source=maps"
      },
      {
        "name": "Достопримечательность в Казани",
        "href": "https://yandex.ru/maps/43/kazan/category/landmark_attraction/89683368508/?utm_medium=mapframe&utm_source=maps"
      }
    ],
    "frame_link": "https://yandex.ru/map-widget/v1/-/CCUAZHX3xB",
    "title": "Казань",
    "phone": "+7-999-22-22222",
    "email": "geeklab@kz.ru",
    "address": "территория Кремль, 11, Казань, Республика Татарстан, Россия"
  },
  {
    "links": [
      {
        "name": "Собор Покрова Пресвятой Богородицы на Рву",
        "href": "https://yandex.ru/maps/org/sobor_pokrova_presvyatoy_bogoroditsy_na_rvu/175159255687/?utm_medium=mapframe&utm_source=maps"
      },
      {
        "name": "Музей в Москве",
        "href": "https://yandex.ru/maps/213/moscow/category/museum/184105894/?utm_medium=mapframe&utm_source=maps"
      }
    ],
    "frame_link": "https://yandex.ru/map-widget/v1/-/CCUAZHh9kD",
    "title": "Москва",
    "phone": "+7-999-33-33333",
    "email": "geeklab@msk.ru",
    "address": "Красная площадь, 7, Москва, Россия"
  }
]"""
)

from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса", help_text="Введите название курса")
    preview = models.ImageField(upload_to="materials/preview", blank=True, null=True, verbose_name="Картинка",
                                help_text="Загрузите изображение")
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса",
                                   help_text="Введите описание курса")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса", help_text="Введите название курса")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name="Курс", help_text="Выберите курс",
                               blank=True, null=True, related_name='lessons')
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса",
                                   help_text="Введите описание курса")
    preview = models.ImageField(upload_to="materials/preview", blank=True, null=True, verbose_name="Картинка",
                                help_text="Загрузите изображение")
    video_url = models.URLField(max_length=200, verbose_name="Ссылка на видео")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

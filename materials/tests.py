from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import Lesson, Course


class MaterialsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(
            name="test_course",
            description="test_description"
            # Убрано поле owner, так как его нет в модели Course
        )
        self.lesson = Lesson.objects.create(
            name="test_lesson",
            course=self.course,
            video_url="https://www.youtube.com/test"  # Обязательное поле
            # Убрано поле owner, если его нет в модели Lesson
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тестирование просмотра урока"""
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    # def test_lesson_create(self):
    #     """Тестирование создания урока"""
    #     url = reverse("materials:lessons_create")
    #     data = {
    #         "name": "Геометрические фигуры",
    #         "course": self.course.id,
    #         "video_url": "https://www.youtube.com/testlesson/",
    #         "description": "Простейшие фигуры",
    #         # preview удалено, так как оно не требуется для создания
    #     }
    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Lesson.objects.all().count(), 2)
    #
    # def test_lesson_update(self):
    #     """Тестирование обновления урока"""
    #     url = reverse("materials:lessons_update", args=(self.lesson.pk,))
    #     data = {"name": "Урок_New"}
    #     response = self.client.patch(url, data)
    #     data = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get("name"), "Урок_New")
    #
    # def test_lesson_delete(self):
    #     """Тестирование удаления урока"""
    #     url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Lesson.objects.all().count(), 0)
    #
    # def test_lesson_list(self):
    #     """Тестирование просмотра списка уроков"""
    #     url = reverse("materials:lessons_list")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     data = response.json()
    #
    #     # Для ListAPIView без пагинации получаем список напрямую
    #     self.assertIsInstance(data, list)
    #     self.assertGreater(len(data), 0)
    #
    #     first_lesson = data[0]
    #     expected_fields = {
    #         "id", "name", "description", "preview",
    #         "video_url", "course"
    #         # Убрано поле owner, если его нет в модели
    #     }
    #
    #     # Проверяем, что все ожидаемые поля присутствуют
    #     self.assertTrue(expected_fields.issubset(first_lesson.keys()))
    #
    #     self.assertEqual(first_lesson["name"], self.lesson.name)
    #     self.assertEqual(first_lesson["course"], self.course.id)
    #
    # def test_lesson_list_filtered_by_course(self):
    #     """Тестирование фильтрации уроков по курсу"""
    #     # Создаем второй курс и урок
    #     course2 = Course.objects.create(
    #         name="test_course2",
    #         description="test_description2"
    #     )
    #     Lesson.objects.create(
    #         name="test_lesson2",
    #         course=course2,
    #         video_url="https://www.youtube.com/test2"
    #     )
    #
    #     # Фильтруем по первому курсу
    #     url = reverse("materials:lessons_list") + f"?pk={self.course.id}"
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     data = response.json()
    #     self.assertEqual(len(data), 1)  # Должен быть только 1 урок для этого курса
    #     self.assertEqual(data[0]["name"], self.lesson.name)

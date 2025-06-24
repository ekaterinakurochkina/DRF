from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import Lesson, Course


class MaterialsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(
            name="test_course", description="test_description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="test_lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тестирование просмотра урока"""
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тестирование создания урока"""
        url = reverse("materials:lessons_create")
        data = {
            "name": "Геометрические фигуры",
            "course": self.course.id,  # Используйте существующий курс
            "video_url": "https://www.youtube.com/testlesson/",
            "description": "Простейшие фигуры",
            "preview": None,
            "payment": {}
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тестирование обновления урока"""
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"name": "Урок_New"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок_New")

    def test_lesson_delete(self):
        """Тестирование удаления урока"""
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тестирование просмотра списка уроков"""
        url = reverse("materials:lessons_list")
        response = self.client.get(url)

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        # Проверка наличия ключа 'results' в ответе
        self.assertIn("results", data)

        results = data["results"]

        # Проверка, что список не пустой (должен содержать созданный в setUp урок)
        self.assertGreater(len(results), 0)

        # Проверка структуры первого урока
        first_lesson = results[0]
        expected_fields = {
            "id", "name", "description", "preview",
            "video_url", "course", "owner"
        }  # Добавьте/удалите поля в соответствии с вашим сериализатором

        # Проверка, что все ожидаемые поля присутствуют
        self.assertEqual(set(first_lesson.keys()), expected_fields)

        # Проверка конкретных значений
        self.assertEqual(first_lesson["name"], self.lesson.name)
        self.assertEqual(first_lesson["course"], self.course.id)
        self.assertEqual(first_lesson["owner"], self.user.id)

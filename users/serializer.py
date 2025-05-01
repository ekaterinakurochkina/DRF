
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from django.db import models
from materials.models import Course, Lesson
from users.models import Payments


# class PaymentsSerializer(ModelSerializer):
#     payments = serializers.SerializerMethodField()
#     course = models.ForeignKey(Course, related_name='payments', null=True, blank=True, on_delete=models.CASCADE)
#     lesson = models.ForeignKey(Lesson, related_name='payments', null=True, blank=True, on_delete=models.CASCADE)
#
#
#     def get_payments(self, payments):
#         related_payments = payments.course.payments.all() if payments.course else payments.lesson.payments.all()
#         # Сериализация связанных платежей
#         return PaymentsSerializer(related_payments, many=True).data
#
#     class Meta:
#         model = Payments
#         fields = ['id', 'user', 'course', 'lesson', 'payment_amount', 'payment_date', 'payments']


class PaymentsSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()

    class Meta:
        model = Payments
        fields = ['id', 'user', 'course', 'lesson', 'payment_amount', 'payment_date', 'payment_method', 'payments']

    def get_payments(self, obj):
        if obj.course:
            related_payments = obj.course.payments.all()  # Получаем все платежи для курса
        elif obj.lesson:
            related_payments = obj.lesson.payments.all()  # Получаем все платежи для урока
        else:
            return []  # Возвращаем пустой список, если нет ни курса, ни урока

        # Сериализация связанных платежей
        return PaymentsSerializer(related_payments, many=True).data




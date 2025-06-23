import secrets

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from materials.models import Course, Lesson
from rest_framework import filters
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
# from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import Payments
from users.models import User
from users.serializer import PaymentsSerializer


class PaymentsCreateApiView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        lesson_id = request.data.get('lesson_id')
        payment_amount = request.data.get('payment_amount')
        payment_method = request.data.get('payment_method', 'transfer')  # Устанавливаем значение по умолчанию

        if course_id:
            course = Course.objects.get(id=course_id)
            payment = Payments.objects.create(user=request.user, course=course, payment_amount=payment_amount,
                                              payment_method=payment_method)
        elif lesson_id:
            lesson = Lesson.objects.get(id=lesson_id)
            payment = Payments.objects.create(user=request.user, lesson=lesson, payment_amount=payment_amount,
                                              payment_method=payment_method)
        else:
            return Response({'error': 'Необходимо указать курс или урок'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PaymentsSerializer(payment).data, status=status.HTTP_201_CREATED)


class PaymentsListApiView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ("course_id", "lesson_id", "payment_method",)


class PaymentsRetrieveApiView(RetrieveAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsUpdateApiView(UpdateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsDestroyApiView(DestroyAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


def logout_view(request):
    logout(request)
    return redirect('mailing:home')


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "user_list.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем всех пользователей и добавляем информацию о принадлежности к группе
        for user in context['users']:
            user.is_manager = user.groups.filter(name="Менеджер").exists()
        return context


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = True
        token = secrets.token_hex(16)  # генерируем токен
        user.token = token
        user.save()


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse_lazy("users:login"))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users:user_form.html"
    success_url = reverse_lazy("users:user_edit")


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "user_confirm_delete.html"
    success_url = reverse_lazy("users:user_list")

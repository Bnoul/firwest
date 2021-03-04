"""
Definition of views.
"""

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import TemplateView
from django.urls import reverse
from .models import User, Choice, Question

import django.contrib.auth.models
import django.contrib.auth.admin


def index(request):
    users = User.objects.all()
    return render(request, "second.html", {"users": users})


def create(request):
    if request.method == "POST":
        user = User()
        user.user = request.POST.get("user")
        user.password = request.POST.get("password")
        user.save()
        return redirect("/")


def edit(request, id):
    try:
        user = User.objects.get(id=id)
        if request.method == "POST":
            user.user = request.POST.get("user")
            user.password = request.POST.get("password")
            user.save()
            return redirect("/")
        else:
            return render(request, "edit.html", {"user": user})
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


# удаление данных из бд
def delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/")


class LoginView(TemplateView):
    template_name = 'login.html'

    def dispath(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("profile"))
            else:
                context['error'] = "Login and password error"
        return render(request, self.template_name, context)


class RegisterView(TemplateView):
    template_name = "register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                User.objects.create_user(username, email, password)
                return redirect(reverse("login"))

        return render(request, self.template_name)


class ProfilePage(TemplateView):
    template_name = "profile.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'myapp/detail.html', {
            'question': question,
            'error_message': "Ничего не выбрано",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('myapp:results', args=(question.id,)))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp/detail.html', {'question': question})


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'myapp/index.html', context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp/results.html', {'question': question})

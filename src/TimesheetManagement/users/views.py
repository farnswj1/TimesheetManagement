from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserCreateForm, UserUpdateForm, ProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
class UserCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User

    def get(self, request, *args, **kwargs):
        user_form = UserCreateForm()
        profile_form = ProfileForm()
        context = {"user_form": UserCreateForm, "profile_form": ProfileForm, "title": "New User"}
        return render(request, "users/create.html", context)

    def post(self, request, *args, **kwargs):
        user_form = UserCreateForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_ = user_form.save(commit=False)
            profile_ = profile_form.save(commit=False)
            profile_.user = user_
            user_.save()
            profile_form.save()
            return redirect("users:user_detail", pk=user_form.instance.pk)
        else:
            return self.get(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_superuser


class DoctorList(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"
    ordering = ["-is_active", "username"]
    queryset = User.objects.filter(is_superuser=False)
    extra_context = {"title": "List of Doctors"}

    def test_func(self):
        return self.request.user.is_superuser


class AdminList(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"
    ordering = ["-is_active", "username"]
    queryset = User.objects.filter(is_superuser=True)
    extra_context = {"title": "List of Administrators"}


class UserDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    context_object_name = "user_"
    template_name = "users/detail.html"
    extra_context = {"title": "User Information"}

    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object()


class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=self.get_object())
        profile_form = ProfileForm(instance=self.get_object().profile)
        context = {"user_form": user_form, "profile_form": profile_form, "title": "Create User"}
        return render(request, "users/update.html", context)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=self.get_object())
        profile_form = ProfileForm(request.POST, instance=self.get_object().profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("users:user_detail", pk=user_form.instance.pk)
        else:
            self.get(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object()


class UserDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    context_object_name = "user_"
    success_url = reverse_lazy("users:user_list")
    extra_context = {"title": "Delete User"}

    def test_func(self):
        return self.request.user.is_superuser and self.request.user != self.get_object()

    def delete(self, request, *args, **kwargs):
        user_ = self.get_object()
        user_.is_active = False
        user_.save()
        return redirect("users:user_detail", pk=user_.pk)
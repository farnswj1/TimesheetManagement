from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserCreationForm, UserUpdateForm, ProfileForm
from django.urls import reverse_lazy

# Create your views here.
class UserCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    template_name = "users/create.html"
    extra_context = {"title": "New Product"}
    form_classes = {"user_form": UserCreationForm, "profile_form": ProfileForm}
    success_url = reverse_lazy("users:user_list")


class UserList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"
    ordering = ["-is_active", "username"]
    extra_context = {"title": "List of Users"}

    def test_func(self):
        return self.request.user.is_superuser


class UserDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    context_object_name = "user_"
    template_name = "users/detail.html"
    extra_context = {"title": "User Information"}

    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object()


class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = "users/update.html"
    context_object_name = "user_"
    extra_context = {"title": "Update User"}
    form_classes = {"user_form": UserCreationForm, "profile_form": ProfileForm}

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm()#instance=request.user)
        profile_form = ProfileForm()#instance=request.user.profile)
        context = {"user_form": user_form, "profile_form": profile_form}
        return render(request, "users/profile.html", context)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save() 
            return reverse_lazy("users:user_list")
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object()

    def get_success_url(self):
        return reverse_lazy("users:user_detail", args=[self.get_object().id])


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
        return self.get_success_url()
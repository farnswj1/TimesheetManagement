from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserCreateForm, UserUpdateForm, ProfileForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .mailers import send_registration_email

# Create your views here.
class UserCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User

    def get(self, request, *args, **kwargs):
        user_form = UserCreateForm()
        profile_form = ProfileForm()
        context = {"user_form": user_form, "profile_form": profile_form, "title": "New User"}
        return render(request, "users/create.html", context)

    def post(self, request, *args, **kwargs):
        user_form = UserCreateForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_ = user_form.save()
            profile_ = profile_form.save(commit=False)
            profile_.user = user_
            profile_form.save()

            send_registration_email(
                user_.email, 
                user_.username, 
                user_form.cleaned_data.get("password1")
            )

            messages.success(self.request, "User has been created!")
            if user_.is_superuser:
                return redirect("users:admin_detail", pk=user_.pk)
            else:
                return redirect("users:doctor_detail", pk=user_.pk)
        else:
            return self.get(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_superuser


class DoctorList(LoginRequiredMixin, ListView):
    model = User
    template_name = "doctors/list.html"
    context_object_name = "users"
    ordering = ["-is_active", "username"]
    extra_context = {"title": "List of Doctors"}
    get_superusers = False
    
    def get_queryset(self):
        first_name = self.request.GET.get("first_name")
        last_name = self.request.GET.get("last_name")
        
        if first_name and last_name:
            queryset = User.objects.filter(
                first_name__icontains=first_name.strip(),
                last_name__icontains=last_name.strip(),
                is_superuser=self.get_superusers
            )
        elif first_name:
            queryset = User.objects.filter(
                first_name__icontains=first_name.strip(), 
                is_superuser=self.get_superusers
            )
        elif last_name:
            queryset = User.objects.filter(
                last_name__icontains=last_name.strip(), 
                is_superuser=self.get_superusers
            )
        else:
            queryset = User.objects.filter(is_superuser=self.get_superusers)
        
        return queryset


class DoctorDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    context_object_name = "user_"
    template_name = "doctors/detail.html"
    extra_context = {"title": "Doctor Information"}

    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object()


class DoctorUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = "doctors/update.html"

    def get(self, request, *args, **kwargs):
        user_ = self.get_object()
        user_form = UserUpdateForm(instance=user_)
        profile_form = ProfileForm(instance=user_.profile)
        context = {
            "user__is_superuser": user_.is_superuser, 
            "user_form": user_form, 
            "profile_form": profile_form, 
            "title": "Update Administrator" if user_.is_superuser else "Update Doctor"
        }
        return self.get_url(request, context)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=self.get_object())
        profile_form = ProfileForm(request.POST, instance=self.get_object().profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_ = user_form.save()
            profile_form.save()
            messages.info(self.request, "User has been updated!")
            
            if user_.is_superuser:
                return redirect("users:admin_detail", pk=user_.pk)
            else:
                return redirect("users:doctor_detail", pk=user_.pk)
        else:
            self.get(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object() and not self.get_object().is_locked()
    
    def get_url(self, request, context):
        return render(request, self.template_name, context)


class DoctorDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "doctors/delete.html"
    context_object_name = "user_"
    success_url = reverse_lazy("users:doctor_list")
    extra_context = {"title": "Delete Doctor"}

    def test_func(self):
        return self.request.user.is_superuser and self.request.user != self.get_object() and not self.get_object().is_locked()

    def delete(self, request, *args, **kwargs):
        user_ = self.get_object()
        user_.is_active = False
        user_.save()
        messages.warning(self.request, "User has been deleted!")

        if user_.is_superuser:
            return redirect("users:admin_list")
        else:
            return redirect("users:doctor_list")


class AdminList(DoctorList):
    template_name = "admins/list.html"
    extra_context = {"title": "List of Administrators"}
    get_superusers = True


class AdminDetail(DoctorDetail):
    template_name = "admins/detail.html"
    extra_context = {"title": "Administrator Information"}


class AdminUpdate(DoctorUpdate):
    template_name = "admins/update.html"


class AdminDelete(DoctorDelete):
    template_name = "admins/delete.html"
    success_url = reverse_lazy("users:admin_list")
    extra_context = {"title": "Delete Administrator"}
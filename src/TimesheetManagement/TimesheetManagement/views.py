from django.shortcuts import redirect

def home(request):
    return redirect("users:doctor_list")
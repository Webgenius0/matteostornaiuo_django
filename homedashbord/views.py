from django.shortcuts import render, HttpResponse

from users.models import User
from client.models import CompanyProfile


def home(request):
    # return HttpResponse("jkldsf")
    return render(request, "home.html")


def dashboard_callback(request, context):

    dashbord_data = {
        "user_data": {
            "total_users": User.objects.count(),
            "total_superusers": User.objects.filter(is_superuser=True).count(),
            "total_clients": User.objects.filter(is_client=True).count(),
            "total_staff": User.objects.filter(is_staff=True).count(),
        }
    }
    context.update({"user_dashbord_data": dashbord_data["user_data"]})

    return context



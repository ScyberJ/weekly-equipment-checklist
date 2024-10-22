from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q
from django.core.mail import send_mail

from .forms import EquipmentRequestForm
from .models import *

# Create your views here.
def home(request):
    return render(request, "base.html")

def request_equipment(request):
    user = request.user
    if not user.is_authenticated:
        redirect(reverse('login'))

    request_pk = request.GET.get("request_pk")
    if request_pk:
        r = Request.objects.get(pk=request_pk)
    else:
        r = Request(requested_by=user)
        r.save()

    return render(request, "request_equipment.html", context={"request": r})


def add_equipment(request, pk):
    r = Request.objects.get(pk=pk)
    equipment_pk = request.GET.get("equipment_pk")
    equipment = None

    if equipment_pk:
        equipment = Equipment.objects.get(pk=equipment_pk)
    
    form = EquipmentRequestForm(initial={"request": r})
    if equipment:
        form = EquipmentRequestForm(instance=equipment) 


    if request.method == "POST":
        form = EquipmentRequestForm(request.POST, initial={"request": r})
        if equipment:
            form = EquipmentRequestForm(request.POST,instance=equipment)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.request = r
            instance.save()


            return redirect(reverse("request-equipment") + f"?request_pk={r.pk}")
        

    return render(request, 'add_equipment.html', context={"request": r, "form": form})

def remove_equipment(request, pk):
    equipment = Equipment.objects.get(pk=pk)

    request_pk = equipment.request.pk

    equipment.delete()

    return redirect(reverse("request-equipment") + f"?request_pk={request_pk}")
    

def submit_request(request, pk):
    r = Request.objects.get(pk=pk)

    r.status = RequestStatus.PENDING

    r.save()

    technicion_email = 'aizaaks@metro.com.na'

    #send mail
    send_mail(
        subject=f"New Request REF#{r.pk}",
        message=f"A new request has been submitted by {r.requested_by.username}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[technicion_email]
    )

    return redirect(reverse("home"))

def list_requests(request):
    user = request.user

    if not user.is_authenticated:
        return redirect(reverse(""))

    requests = Request.objects.filter(~Q(status=RequestStatus.INACTIVE))

    if not user.is_superuser:
        requests = requests.filter(requested_by=user)

    return render(request, "list_requests.html", context={"requests": requests})
    
def mark_as_done(request, pk):
    r = Request.objects.get(pk=pk)
    r.status = RequestStatus.FIXED
    r.save()

    #send email
    send_mail(
        subject=f"Request Done REF#{r.pk}",
        message="Your request has been fulfilled. The problems you stated in your request should be solved. Have a nice day.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[r.requested_by.email]
    )

    return redirect(reverse("list-requests"))

def request_detail(request, pk):
    r = Request.objects.get(pk=pk)

    return render(request, "request_detail.html", context={"request": r})

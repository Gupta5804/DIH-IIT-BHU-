from django.shortcuts import render, get_object_or_404, redirect
from .models import Lost,Found
from .forms import LostForm,FoundForm
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def report_lost(request):
    form = LostForm(request.POST or None, request.FILES or None)
    if not request.user.is_authenticated():
        raise Http404
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request, "lost_found/report_lost.html", {
        "form": form,
    })
def report_found(request):
    form = FoundForm(request.POST or None, request.FILES or None)
    if not request.user.is_authenticated():
        raise Http404
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request, "lost_found/report_found.html", {
        "form": form,
    })


def list_item(request):
    queryset_list_lost = Lost.objects.all()
    queryset_list_found = Found.objects.all()
    paginator = Paginator(queryset_list_lost ,25)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        queryset_lost = paginator.page(page)
    except PageNotAnInteger:
        queryset_lost = paginator.page(1)
    except EmptyPage:
        queryset_lost = paginator.page(paginator.num_pages)
    paginator = Paginator(queryset_list_found, 25)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        queryset_found = paginator.page(page)
    except PageNotAnInteger:
        queryset_found = paginator.page(1)
    except EmptyPage:
        queryset_found = paginator.page(paginator.num_pages)


    return render(request, "lost_found/list.html", {
        "title": "List",
        "obj_list_lost": queryset_lost,
        "obj_list_found":queryset_found
    })


def detail_lost(request, id=None):
    instance= get_object_or_404(Lost, id=id)

    return render(request, "lost_found/detail_l.html", {
        "title": instance.title,
        "instance": instance,
    })

def detail_found(request, id=None):
    instance= get_object_or_404(Found, id=id)

    return render(request, "lost_found/detail_f.html", {
        "title": instance.title,
        "instance": instance,
    })


def edit_lost(request, id=None):
    instance = get_object_or_404(Lost, id=id)
    form = LostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Changes Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request, "lost_found/report_lost.html", {
        "title": instance.title,
        "instance": instance,
        "form": form,
    })


def delete_item(request, id=None):
    instance = get_object_or_404(Lost, id=id)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("laf:list")



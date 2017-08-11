from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth import login,authenticate

from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
import os
from django.conf import settings as django_settings
from PIL import Image


def site_redirect(request):
    return redirect('/accounts/login')

@login_required(login_url="accounts/login")
def home(request):
    return redirect('/feeds/')


@login_required
def edit_user(request, pk):
    user = User.objects.get(id=pk)
    user_form = UserProfileForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile,fields=( 'bio', 'phone', 'city', 'branch','year'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileForm(request.POST,  instance=user)
            formset = ProfileInlineFormset(request.POST,  instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/accounts/profile/')

        return render(request, "profile_edit.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied

@login_required
def get_user(request,pk):
    user = User.objects.get(id=pk)
    return render(request, 'profile_view.html', {"user": user})


@login_required
def profile(request, username):
    page_user = get_object_or_404(User, username=username)
 #  paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
  #  feeds = paginator.page(1)
#    from_feed = -1
 #   if feeds:
   #     from_feed = feeds[0].id
    return render(request, 'core/profile.html', {
        'page_user': page_user,
     #   'feeds': feeds,
      #  'from_feed': from_feed,
        'page': 1
        })
@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True

    except Exception:
        pass

    return render(request, 'core/picture.html',
                  {'uploaded_picture': uploaded_picture})
@login_required
def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('/settings/picture/?upload_picture=uploaded')

    except Exception as e:
        print(e)
        return redirect('/settings/picture/')

@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
            request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
            request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)

    except Exception:
        pass

    return redirect('/settings/picture/')

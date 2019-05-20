from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse, redirect
from accounts.forms import SignUpForm, EditProfileForm, UploadForm
from accounts.models import UserProfile, ItemData, RequestData, ClaimData
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Create your views here.

email_message ='Dear admin,\n\n\
There is a new image upload for "found items".\n\
Please verify the image and check the "IsValid" checkbox for that image\n\n\
Thank you.'
subject = 'New Image upload'
from_email = settings.EMAIL_HOST_USER
to_email = from_email#'shrikant_goswami@spit.ac.in' 

@login_required(login_url='/accounts/login/')
def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            send_mail(subject, email_message, from_email, [to_email], fail_silently=False)
            form.save()
            messages.info(request, 'Your image is uploaded and waiting for admin approval, Thank you')
            return render(request, 'accounts/upload.html', {'form': UploadForm()})
    else:
        form = UploadForm()
    return render(request, 'accounts/upload.html', {'form': form})


@login_required(login_url='/accounts/login/')
def claim(request, id):
    item = get_object_or_404(ItemData, pk=id)
    status = False
    post1 = False
    if request.method == 'POST':
        location_claim = request.POST.get('Location').lower()
        itemid = ItemData.objects.get(pk=request.POST.get('ItemID'))
        location_act = itemid.Location.lower()
        post1 = True
        if location_act in location_claim or location_claim in location_act:
            status = True
            obj = ClaimData(
                UserID=request.user,
                Location=location_claim,
                ItemID=ItemData.objects.get(pk=request.POST.get('ItemID')),
            )
            obj.save()
    return render(request, 'accounts/claim.html', {'item': item, 'status': status, 'post': post1})


@login_required(login_url='/accounts/login/')
def home(request):
    data = ItemData.objects.all().filter(Isvalid=True)
    return render(request, 'accounts/home.html', {'data': data})


def register(request):
    print('Hello')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print('Hello')

        if form.is_valid():
            objuser = form.save()

            print(objuser.id)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            print(request.user.id)

            objt = UserProfile(user=objuser, UID=request.POST.get('UID'), branch=request.POST.get('Branch'),
                               year=request.POST.get('Year'), contactno=request.POST.get('ContactNo'))

            print(objt)

            objt.save()

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('login'))

    else:
        form = SignUpForm()

    print('Hello')
    return render(request, 'accounts/signup.html', {'form': form})


@login_required(login_url='/accounts/login/')
def profile(request):
    obj = UserProfile.objects.get(user_id=request.user.id)
    args = {'UID': obj.UID, 'contactno': obj.contactno,
            'branch': obj.branch, 'year': obj.year}
    return render(request, 'accounts/profile.html', args)


@login_required(login_url='/accounts/login/')
def editprofile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/editprofile.html', args)


@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts/profile')
        else:
            return redirect('accounts/change-password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


@login_required(login_url='/accounts/login/')
def requestItem(request):
    # args = {'UID': request.POST.get('UID')}
    # print(request.POST.get('UID'))
    # print(request.POST.get('desc'))
    # print(request.POST.get('loc'))
    # obj = RequestData(UID=request.POST.get('UID'),Description=request.POST.get('desc'),Location=request.POST.get('loc'))
    # obj.save()
    print(request.user.id)

    submitButton = request.POST.get('Submit')
    if submitButton == 'Submit':
        obj = RequestData(UID=request.POST.get('UID'), Description=request.POST.get(
            'Description'), Location=request.POST.get('Location'))
        obj.save()
    return render(request, 'accounts/requestitem.html')

def guide_view(request):
  return render(request, 'accounts/guide.html')
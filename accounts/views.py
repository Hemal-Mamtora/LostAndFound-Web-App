from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse, redirect
from accounts.forms import SignUpForm, EditProfileForm, UploadForm
from accounts.models import UserProfile, ItemData, RequestData, ClaimData
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.


def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid(): 
            form.save() 
            return redirect(request, 'accounts/home.html')
    else: 
        form = UploadForm() 
    return render(request, 'accounts/upload.html', {'form' : form}) 


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


def home(request):
    data = ItemData.objects.all()
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
            return redirect('http://127.0.0.1:8000/accounts')

    else:
        form = SignUpForm()

    print('Hello')
    return render(request, 'accounts/signup.html', {'form': form})


def profile(request):
    obj = UserProfile.objects.get(user_id=request.user.id)
    args = {'UID': obj.UID, 'contactno': obj.contactno,
            'branch': obj.branch, 'year': obj.year}
    return render(request, 'accounts/profile.html', args)


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

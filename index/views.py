from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import EditProfileForm

# Create your views here.

def homepage(request):
    return render(request, 'index/homepage.html')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		print("Errors", form.errors)
		if form.is_valid():
			form.save()
			return redirect('/')
		else:
			return render(request, 'registration/register.html', {'form':form})
	else:
		form = UserCreationForm()
		context = {'form': form}
		return render(request, 'registration/register.html', context)

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # 這裡你可以添加邏輯來處理表單數據，例如發送郵件
        send_mail(
            f"Contact Form Submission from {name}",
            message,
            email,
            [settings.DEFAULT_FROM_EMAIL],  # 發送到你的郵箱
        )
        return HttpResponse("Thank you for your message.")

    return render(request, 'contact.html')

@login_required
def member_center(request):
    return render(request, 'member_center.html', {
        'user': request.user
    })

@login_required
def view_profile(request):
    return render(request, 'view_profile.html', {
        'user': request.user
    })

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
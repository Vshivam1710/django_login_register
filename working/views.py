from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from working.forms import LoginForm, RegisterFrom
from django.contrib.auth.hashers import make_password, check_password
from working.models import Register as RegisterModel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import datetime


def registered():
    count = RegisterModel.objects.all().count()
    return count


def home(request):
    if request.session.get('_auth_user_id') is not None:
        if RegisterModel.objects.filter(pk=request.session.get('_auth_user_id')).exists():
            data = RegisterModel.objects.get(pk=request.session.get('_auth_user_id'))
            return render(request, 'index.html', {'data': data, 'count': registered()}, status=200)
        return render(request, 'index.html', {'not_login': True, 'count': registered()}, status=200)
    else:
        return render(request, 'index.html', {'not_login': True, 'count': registered()}, status=200)


class Login(View):
    form = LoginForm()

    def get(self, request, message=None):
        if message is None:
            if request.session.get('_auth_user_id') is None:
                return render(request, 'login.html', {'form': self.form, 'not_login': True, 'count': registered()}, status=200)
            else:
                return redirect('/')
        else:
            if request.session.get('_auth_user_id') is None:
                return render(request, 'login.html', {'form': self.form, 'not_login': True, 'count': registered(), 'error': message}, status=200)

    def post(self, request):
        self.form = LoginForm(request.POST)
        if self.form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            if RegisterModel.objects.filter(username__icontains=username).exists():
                if check_password(password, RegisterModel.objects.get(username__icontains=username).password):
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        update = RegisterModel(pk=user.pk, last_login=datetime.datetime.now())
                        update.save(update_fields=['last_login'])
                        login(request, user)
                        return redirect('/')
                else:
                    return self.get(request, 'invalid_password')
            else:
                return self.get(request, 'invalid_email')


@method_decorator(csrf_exempt, name='dispatch')
class Register(View):
    form = RegisterFrom()

    def get(self, request):
        if request.session.get('_auth_user_id') is None:
            return render(request, 'register.html', {'form': self.form, 'not_login': True, 'count': registered()}, status=200)
        else:
            return redirect('/')

    def post(self, request):
        self.form = RegisterFrom(request.POST)
        if self.form.is_valid():
            f = self.form.save(commit=False)
            f.first_name = request.POST['first_name']
            f.last_name = request.POST['last_name']
            f.email = request.POST['email']
            f.password = make_password(request.POST['password'])
            f.mobile = request.POST['mobile']
            f.is_superuser = True
            f.username = request.POST['first_name']
            f.is_staff = True
            f.is_active = True
            self.form.save()
            return redirect('/login/')
        return HttpResponse(self.form.errors, status=400)


@login_required
def my_logout(request):
    logout(request)
    return redirect('/')


@csrf_exempt
@login_required
def update_password(request):
    if request.method == 'POST':
        if check_password(request.POST['o_pass'], RegisterModel.objects.get(pk=request.session.get('_auth_user_id')).password):
            if request.POST['n_pass'] == request.POST['c_pass']:
                update = RegisterModel.objects.get(pk=request.session.get('_auth_user_id'))
                update.set_password(request.POST['n_pass'])
                update.save()
                return redirect('/logout/')


@method_decorator(csrf_exempt, name='dispatch')
class EditProfile(View):
    def get(self, request, pk):
        if request.session.get('_auth_user_id') is not None:
            if RegisterModel.objects.filter(pk=pk).exists():
                if RegisterModel.objects.get(pk=pk).pk == int(request.session.get('_auth_user_id')):
                    data = RegisterModel.objects.get(pk=pk)
                    return render(request, 'edit_profile.html', {'data': data, 'count': registered()}, status=200)
                return HttpResponse(status=400)
            return HttpResponse(status=204)
        else:
            return redirect('/logout/')

    @csrf_exempt
    def post(self, request, pk):
        update = RegisterModel(
            pk=pk, username=request.POST['u_name'],
            first_name=request.POST['f_name'],
            last_name=request.POST['l_name'],
            mobile=request.POST['mobile']
                               )
        update.save(update_fields=['username', 'first_name', 'last_name', 'mobile'])
        return redirect('/')


@csrf_exempt
@login_required
def delete_data(request, pk):
    if request.session.get('_auth_user_id') is not None:
        if RegisterModel.objects.filter(pk=pk).exists():
            if RegisterModel.objects.get(pk=pk).pk == int(request.session.get('_auth_user_id')):
                if check_password(request.POST['password'], RegisterModel.objects.get(pk=pk).password):
                    data = RegisterModel.objects.get(pk=pk)
                    logout(request)
                    data.delete()
                    return redirect('/')
            return HttpResponse(status=400)
        return HttpResponse(status=204)
    else:
        return redirect('/logout/')

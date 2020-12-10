# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET

from employees.forms import EmployeeForm
from managers.models import Users

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    employee_form = EmployeeForm(request.POST or None)
    employee_data = Users.objects.filter(is_employee=True)
    context = {
        'employee_form': employee_form,
        'employee': employee_data
    }
    return render(request, 'dashboard.html', context)


@require_POST
def save_employee(request):
    signup_form = EmployeeForm(request.POST)
    password = request.POST.get('password')
    if signup_form.is_valid():
        instance = signup_form.save(commit=False)
        instance.set_password(password)
        instance.is_employee = True
        instance.save()
        messages.success(request, 'Success! Account Created.')
        return redirect('/dashboard/')
    else:
        print(signup_form.errors)
        signup_form = EmployeeForm(request.POST)
        context = {
            'employee_form': signup_form
        }
        return render(request, 'dashboard.html', context)


@require_GET
def delete_emp(request, emp_id=None):
    emp_obj = Users.objects.get(id=emp_id)
    emp_obj.delete()
    messages.success(request, 'Employee deleted.')
    return redirect('/dashboard/')

@login_required
@require_GET
def update_emp(request, emp_id=None):
    employee_form = EmployeeForm(request.POST or None)
    employee_data = Users.objects.filter(is_employee=True)

    emp_obj = get_object_or_404(Users, id=emp_id)
    update_emp_form = EmployeeForm(request.POST or None, instance=emp_obj)

    # if form.is_valid():
    #     form.save()
    # else:
    #     print(form.errors)
    context = {
        'update_emp_form': update_emp_form,
        'employee_form': employee_form,
        'employee': employee_data,
        'emp_obj': emp_obj
    }
    return render(request, 'dashboard.html', context)


@require_POST
def save_update_emp(request, emp_id=None):
    emp_obj = get_object_or_404(Users, id=emp_id)
    update_emp_form = EmployeeForm(request.POST or None, instance=emp_obj)
    employee_form = EmployeeForm(request.POST or None)
    employee_data = Users.objects.filter(is_employee=True)

    if update_emp_form.is_valid():
        update_emp_form.save()
        messages.success(request, 'Employee updated.')
        return redirect('/dashboard/')
    else:
        print(update_emp_form.errors)
        context = {
            'update_emp_form': update_emp_form,
            'employee_form': employee_form,
            'employee': employee_data,
        }
        return render(request, 'dashboard.html', context)

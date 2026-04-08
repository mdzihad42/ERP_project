from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department, Position, UnitNumber
from .forms import DepartmentForm, PositionForm, UnitNumberForm

# --- Unit Numbers CRUD ---
def admin_unit_list(request):
    units = UnitNumber.objects.all().select_related('city', 'city__state', 'city__state__country')
    return render(request, 'management/unit_list.html', {'units': units})

def admin_unit_create(request):
    form = UnitNumberForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Unit created successfully.")
        return redirect('admin_unit')
    return render(request, 'management/unit_form.html', {'form': form, 'title': 'Create Unit'})

def admin_unit_edit(request, pk):
    unit = get_object_or_404(UnitNumber, pk=pk)
    form = UnitNumberForm(request.POST or None, instance=unit)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Unit updated successfully.")
        return redirect('admin_unit')
    return render(request, 'management/unit_form.html', {'form': form, 'title': 'Edit Unit'})

# --- Department CRUD ---
def admin_department_list(request):
    departments = Department.objects.all().select_related('unit')
    return render(request, 'management/department_list.html', {'departments': departments})

def admin_department_create(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Department created successfully.")
        return redirect('admin_department')
    return render(request, 'management/department_form.html', {'form': form, 'title': 'Create Department'})

def admin_department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=dept)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Department updated successfully.")
        return redirect('admin_department')
    return render(request, 'management/department_form.html', {'form': form, 'title': 'Edit Department'})

# --- Position CRUD ---
def admin_position_list(request):
    positions = Position.objects.all().select_related('department', 'department__unit')
    return render(request, 'management/position_list.html', {'positions': positions})

def admin_position_create(request):
    form = PositionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Position created successfully.")
        return redirect('admin_position')
    return render(request, 'management/position_form.html', {'form': form, 'title': 'Create Position'})

def admin_position_edit(request, pk):
    pos = get_object_or_404(Position, pk=pk)
    form = PositionForm(request.POST or None, instance=pos)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Position updated successfully.")
        return redirect('admin_position')
    return render(request, 'management/position_form.html', {'form': form, 'title': 'Edit Position'})

# --- Simple Delete view generator ---
def admin_delete(request, model_name, pk):
    models = {'unit': UnitNumber, 'department': Department, 'position': Position}
    model = models.get(model_name)
    instance = get_object_or_404(model, pk=pk)
    instance.delete()
    messages.success(request, f"{model_name.capitalize()} deleted successfully.")
    return redirect(f'admin_{model_name}')

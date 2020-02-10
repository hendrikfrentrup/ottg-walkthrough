from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm

import os
current_pid = os.getpid()
print(f'loading lists view module (PID:{current_pid})', flush=True)

def home_page(request):
    print(f'home page view (PID:{current_pid})', flush=True)
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    print(f'list view: id {list_id} (PID:{current_pid})', flush=True)
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {"list": list_, 'form': form})

def new_list(request):
    print(f'new list view (PID:{current_pid})', flush=True)
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})
    
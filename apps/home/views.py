# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import generic

from .forms import FruitForm

from apps.home.models import Fruit

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    return render(request, 'home/index.html', context)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        if load_template == 'fruits.html':
            fruits = Fruit.objects.all()
            context['fruits'] = fruits

        if load_template == 'fruits_add.html':
            form = FruitForm(request.POST or None)
            msg = None

            if request.method == "POST":
                if form.is_valid():
                    name = form.cleaned_data.get("name")
                    description = form.cleaned_data.get("description")
                    image = form.cleaned_data.get("image")
                    f = Fruit.objects.create(name=name, description=description, image=image)
                    f.save()
                    return redirect("/fruits.html")
                else:
                    msg = 'Erreur lors de la validation du formulaire'

            return render(request, "home/fruits_add.html", {"form": form, "msg": msg})

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
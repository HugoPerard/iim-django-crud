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
from django.utils import timezone

from .forms import FruitForm, ChatForm

from apps.home.models import Fruit, Chat

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

        if 'fruits_edit' in request.path:
            fruitId = load_template
            currentFruit = Fruit.objects.filter(id=fruitId)
            form = FruitForm(request.POST or None)
            form.fields['name'].initial = currentFruit[0].name
            form.fields['description'].initial = currentFruit[0].description
            form.fields['image'].initial = currentFruit[0].image
            msg = None

            if request.method == "POST":
                if form.is_valid():
                    name = form.cleaned_data.get("name")
                    description = form.cleaned_data.get("description")
                    image = form.cleaned_data.get("image")
                    f = currentFruit.update(name=name, description=description, image=image)
                    return redirect("/fruits.html")
                else:
                    msg = 'Erreur lors de la validation du formulaire'

            return render(request, "home/fruits_edit.html", {"form": form, "msg": msg, "fruitId": fruitId})

        if load_template == 'messagerie.html':
            messages = Chat.objects.order_by('-pub_date')[:20]
            form = ChatForm(request.POST or None)
            msg = None

            if request.method == "POST":
                if form.is_valid():
                    text = form.cleaned_data.get("text")
                    logger.error("-----_______----", text)
                    author = request.user.username
                    pub_date = timezone.now()
                    c = Chat.objects.create(text=text, author=author, pub_date=pub_date)
                else:
                    msg = 'Erreur lors de la validation du formulaire'

            return render(request, "home/messagerie.html", {"form": form, "msg": msg, "messages": messages, "user": request.user.username})

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
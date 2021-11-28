# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class FruitForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nom",
                "class": "form-control"
            }
        ))
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Description",
                "class": "form-control"
            }
        ))
    image = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Url d'image",
                "class": "form-control"
            }
        ))

class ChatForm(forms.Form):
    text = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Message",
                "class": "form-control"
            }
        ))

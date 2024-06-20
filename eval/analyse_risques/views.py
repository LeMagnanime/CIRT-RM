from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from . import forms 
from .models import *

from django.contrib import messages

from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
openai.api_key = 'API_KEY'

def get_gpt_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        
        # Configurer la clé API OpenAI
        openai.api_key = os.getenv('API_KEY')
        
        try:
            # Effectuer une requête à l'API OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            
            # Extraire la réponse générée par le modèle
            gpt_response = response.choices[0].message['content']
            
            return JsonResponse({'response': gpt_response})
        
        except openai.error.OpenAIError as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

# Create your views here.
def home2(request):
    form = forms.AssetForm()
    actifs = Asset.objects.all()
    message = ""
    errors = ''
    if request.method == 'POST':
        form = forms.AssetForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Les actifs ont bien été enregistré"
            messages.success(request, message)
            return redirect('home2')
    else:
        errors = form.errors
        
    context = {
        'form': form,
        'actifs': actifs
    }
        
    return render(request, "analyse_risques/AssetsList.html", context)

def vulnerabilite(request):
    actifs = Asset.objects.all()
    form = forms.AnalyseForm()

    if request.method == 'POST': 
        form = forms.AnalyseForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False) 
            evaluation.save()
            return redirect('vulnerabilite')
        else:
            print(form.errors)

    context = {
        'actifs': actifs,
        'form': form,
    }
    
    return render(request, "analyse_risques/analyse.html", context)

def exemple(request):
    return render(request, "exemple.html")

def essaie(request):
    if request.method == 'POST':
        # Récupérer le texte de l'utilisateur à partir du formulaire
        user_input = request.POST.get('user_input')

        # Envoyer la requête à l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        # Récupérer la réponse
        ai_response = response['choices'][0]['message']['content'].strip()

        # Passer la réponse à votre template
        return render(request, 'analyse_risques/essaie.html', {'response': ai_response, 'user_input': user_input})
    
    return render(request, 'analyse_risques/essaie.html')


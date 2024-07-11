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
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from .models import Asset, EvaluationRisque
openai.api_key = 'API_KEY'

genai.configure(api_key="AIzaSyBtzqb51YGOAWy9a5zCvNcvEfST3NHvvKY")

generation_config = {
  "temperature": 0.4,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  safety_settings = {HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : HarmBlockThreshold.BLOCK_NONE},
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  )
chat_session = model.start_chat(
    history=[]
)

def get_gpt_response(request):
    #print("1")
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        
        # Configurer la clé API OpenAI
        openai.api_key = os.getenv('API_KEY')
        print(user_input)
        response = chat_session.send_message(user_input)
            
            # Extraire la réponse générée par le modèle
        gpt_response = response.text
        #print(response)
        return JsonResponse({'response': gpt_response})
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


def registre_risque(request):
    actifs = Asset.objects.all()
    context = {
        'actifs': actifs, 
    }
    return render(request, "analyse_risques/registreRisque.html", context)

def exemple(request):
    return render(request, "exemple.html")


def essaie(request):
    risques = EvaluationRisque.objects.select_related('actif').all()
    risques_par_actif = {}
    for risque in risques:
        if risque.actif not in risques_par_actif:
            risques_par_actif[risque.actif] = []
        risques_par_actif[risque.actif].append(risque)
    
    context = {
        'risques_par_actif': risques_par_actif
    }

    return render(request, 'analyse_risques/essaie.html', context)

def Rapport(request):
    return render(request, "analyse_risques/Rapport.html")

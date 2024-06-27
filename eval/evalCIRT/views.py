from django.shortcuts import render, redirect, get_list_or_404 , get_object_or_404
from django.http import HttpResponse, FileResponse, Http404
from .forms import CompanyForm
from django.forms import ModelForm
from .forms import DocumentForm
from .models import DocumentAdmin
from .models import Document
from .models import Donnee
from .forms import DonneeForm
from django.shortcuts import render 
from django.template.loader import render_to_string
from bs4 import BeautifulSoup
import os
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from flask import Flask, request, render_template_string
import subprocess
# Create your views here.
from django.shortcuts import render
import os
import pandas

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key="AIzaSyBtzqb51YGOAWy9a5zCvNcvEfST3NHvvKY")

# Créez le répertoire s'il n'existe pas
#media_root = settings.MEDIA_ROOT
#documents_dir = os.path.join(media_root, 'document')
#if not os.path.exists(documents_dir):
    #os.makedirs(documents_dir)

def login_view(request):
    
    return render(request, 'home.html')
def home(request):
    return render(request, 'home.html', {'name': request.user.username})


def dashboard(request):
    return render(request, "dashboard.html")

def ancien_projet(request):
    # Logique pour récupérer les anciens projets depuis la base de données
    projects = ["Ancien projet 1", "Ancien projet 2", "Ancien projet 3"]
    return render(request, 'ancien_projet.html', {'projects': projects})

def nouveau_projet(request):
    # Logique pour afficher le formulaire pour un nouveau projet
    return render(request, 'nouveau_projet.html') 



def analyse_quantitative(request):
    return render(request, 'analyse_quantitative.html')

def analyse_qualitative(request):
    return render(request, 'analyse_qualitative.html')

def analyse_quantitative(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home2')  # page de redirection a definir
    else:
        form = CompanyForm()
    return render(request, 'analyse_quantitative.html',{'form':form})

def AssetsList(request):
    return render(request, 'AssetsList.html')

def tableau_vulnerabilite(request):
    return render(request, 'tableau_vulnerabilite.html')

def diagram(request):
    return render(request, 'diagram.html')

def index(request):
    return render(request, 'index.html')

def analyse_qualitative(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referentiel')  # Redirige vers la vue suivante après avoir enregistré les données de l'entreprise
    else:
        form = CompanyForm()
    return render(request, 'analyse_qualitative.html',{'form':form})



# définir une méthode qui génère la vue
def referentiel(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
           
            return redirect('referentiel')
    else:
        form = DocumentForm()
    return render(request, 'referentiel.html', {'form': form , 'referentiel_Document':Document.objects.all})
    # pointer vers le fichier du template index.html

@xframe_options_exempt
def analyse(request,document_name):
   # Récupérer le document à partir du nom de fichier
    file_path = 'doument/' + document_name
    print(file_path)

    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        # Renvoie une erreur 404 si le fichier n'existe pas
        return HttpResponseNotFound('Le fichier demandé n\'existe pas')

    # Renvoie le fichier demandé
    return sendfile(request, file_path)

def document_view(request,):
    document = Document.objects.get(id=document_id)
    return render(request, 'analyse.html', {'document': document})

@xframe_options_exempt
def analyse(request,document_name,):
    print('okk')
     # Récupérer le document à partir du nom de fichier
    doc = pandas.read_excel('./eval/Documents/document/questionnaire_iso_das.xlsx')
    doc = doc.to_html()

    if request.method == 'POST':
        form = DonneeForm(request.POST)
        if form.is_valid():
            form.save()
    
            return redirect('analyse', pk=tableau.pk)
    else:
        form = DonneeForm()
    donnees = Donnee.objects.all()
    
    return render(request, 'analyse.html', {'form': form, 'donnees': donnees,  'file': document_name, 'doc': doc})

    @xframe_options_exempt
    def analyse(request,):
        print('tt')
        if request.method == 'POST':
            form = DonneeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('analyse', pk=tableau.pk)
        else:
            form = DonneeForm()
    return render(request, 'analyse.html', {'form': form})



def serve_flask_app(request):
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        result = ""
        nusmv_code = ""
        if request.method == 'POST':
            nusmv_code = request.form['nusmv_code']
            result = run_nusmv(nusmv_code)
        return render_template_string(template, nusmv_code=nusmv_code, result=result)

    def run_nusmv(nusmv_code):
        file_path = 'model.smv'
        nusmv_path = 'C:/Program Files/NuSMV-2.6.0-win64/NuSMV-2.6.0-win64/bin/NuSMV.exe'
        with open(file_path, 'w') as f:
            f.write(nusmv_code)
        try:
            result = subprocess.run([nusmv_path, file_path], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"An error occurred: {e.stderr}"
        except FileNotFoundError:
            return "NuSMV executable not found. Please ensure it is installed and the path is correct."

    return HttpResponse(app.run(debug=True))


from .utils import run_nusmv

def index(request):
    result = ""
    nusmv_code = ""
    if request.method == 'POST':
        nusmv_code = request.POST.get('nusmv_code', '')
        result = run_nusmv(nusmv_code)
    return render(request, 'index.html', {'nusmv_code': nusmv_code, 'result': result})

#def index(request):
   # return render(request, 'index.html')


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
chat_session = model.start_chat()

def get_gpt_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        
        # Configurer la clé API OpenAI
        #openai.api_key = os.getenv('API_KEY')
        
        try:
            # Effectuer une requête à l'API OpenAI
            response = chat_session.send_message(user_input)
            
            # Extraire la réponse générée par le modèle
            gpt_response = response.text
            print(gpt_response)
            return JsonResponse({'response': gpt_response})
        
        except openai.error.OpenAIError as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)



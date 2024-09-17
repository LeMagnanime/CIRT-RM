import subprocess

def run_nusmv(nusmv_code):
    file_path = 'model.smv'
    nusmv_path = 'C:/NuSMV-2.6.0-win64/NuSMV-2.6.0-win64/bin/NuSMV.exe'  # Chemin vers l'exécutable NuSMV
    with open(file_path, 'w') as f:
        f.write(nusmv_code)
    try:
        result = subprocess.run([nusmv_path, file_path], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Une erreur s'est produite : {e.stderr}"
    except FileNotFoundError:
        return "Exécutable NuSMV introuvable. Veuillez vous assurer qu'il est installé et que le chemin est correct."

from flask import Flask, redirect, render_template, url_for, request, session
from dotenv import load_dotenv, set_key, dotenv_values
from urllib.parse import urljoin, urlparse
from flask_babel import Babel, gettext as _
import json 
import markdown
import os
app = Flask(__name__)

chemin_env="static/.env"

def isThereASecretKey() :
    vals = dotenv_values(chemin_env)
    return bool(vals.get("SECRET_KEY", ""))

def setSecretKey(key) :
    #Enregistrement de la clef secrete
    load_dotenv(chemin_env) #Ouverture du .env
    set_key(chemin_env, "SECRET_KEY", key) #on enregistre

def getSecretKey() :
    vals = dotenv_values(chemin_env)
    return vals.get("SECRET_KEY", "")

if not isThereASecretKey(): #Si pas de clef secrete (utilisée pour les sessions)
    # Générer une clé secrète aléatoire et la stocker dans le .env
    secret_key = os.urandom(24).hex()
    setSecretKey(secret_key)#Enregistrer la clef dans le .env
    app.secret_key=secret_key #Enregistrer la clef dans l'app
else :
    app.secret_key=getSecretKey() #Lire la clef dans le .env et l'enregistrer dans l'app


app.config['BABEL_DEFAULT_LOCALE'] = 'en'

def get_locale():
    # Utilise la langue choisie par l'utilisateur (stockée en session)
    return session.get('lang', 'fr')

babel = Babel(app, locale_selector=get_locale)

def load_json_from_static(filename='static/projects.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@app.context_processor
def inject_projects():
    # injecter les projets chargés depuis le fichier JSON dans tous les templates
    return {
        'projects': load_json_from_static(),
        'current_lang': get_locale()
    }

def is_safe_url(target):
    host_url = request.host_url
    ref_url = urlparse(host_url)
    test_url = urlparse(urljoin(host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<int:project_id>')
def project(project_id):
    with open(load_json_from_static()[project_id-1]['details']+f"_{get_locale()}.md", encoding='utf-8') as details_file:
            details_md = details_file.read()
    return render_template('project_detail.html', id=int(project_id), details_md=markdown.markdown(details_md))

@app.route('/switchlanguage')
def switchlanguage():
    session['lang'] = 'en' if session.get('lang', 'fr') == 'fr' else 'fr'
    
    # récupère la page de retour fournie par le template
    next_url = request.args.get('next') or url_for('index')
    
    # sécurité : n'autorise que les redirections internes
    if not is_safe_url(next_url):
        next_url = url_for('index')
    return redirect(next_url)


def load_experiences_from_static(filename='static/experiences.json'):
    """Charge la liste d'expériences depuis static/experiences.json si présent, sinon retourne une liste d'exemples."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Exemples simples — tu pourras les remplacer par un fichier JSON dans static/
        return [
            {
                "image": url_for('static', filename='projects/1/cover.jpg'),
                "start": "2023-09",
                "end": "2025-06",
                "title": "Ingénieur Développement",
                "organisation": "Entreprise Exemple",
                "location": "Paris, France",
                "description": "Travail sur des applications web en Python/Flask, conception d'APIs et mise en place de tests.",
                "type": "pro"
            },
            {
                "image": url_for('static', filename='projects/1/cover.jpg'),
                "start": "2019-09",
                "end": "2023-06",
                "title": "Licence Informatique",
                "organisation": "Université Exemple",
                "location": "Lyon, France",
                "description": "Parcours orienté développement logiciel et systèmes.",
                "type": "education"
            }
        ]


@app.route('/cv')
def cv():
    # Charger les expériences (fichier static/experiences.json facultatif)
    experiences = load_experiences_from_static()
    return render_template('cv.html', experiences=experiences)


def save_contact_to_static(entry, filename='static/contacts.json'):
    """Ajoute une entrée de contact à static/contacts.json (crée le fichier si absent)."""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    data.append(entry)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    error = None
    success = None
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        message = (request.form.get('message') or '').strip()

        if not name or not email or not message:
            error = _('Veuillez remplir tous les champs.')
        else:
            entry = {
                'name': name,
                'email': email,
                'message': message,
                'path': request.path
            }
            try:
                save_contact_to_static(entry)
                success = _('Message envoyé — merci !')
            except Exception as e:
                error = _('Une erreur est survenue lors de l\'enregistrement.')

    return render_template('contact.html', error=error, success=success)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
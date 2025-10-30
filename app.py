from flask import Flask, redirect, render_template, url_for
from flask_babel import Babel, gettext as _
import json 
app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'

langue='fr'
def get_locale():
    # Utilise la langue choisie par l'utilisateur (stockée en session)
    return langue

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


@app.route('/')
def index():
    print(load_json_from_static())
    # Exemple de données pour les projets
    return render_template('index.html')

@app.route('/switchlanguage')
def switchlanguage():
    global langue
    langue = 'en' if langue == 'fr' else 'fr'
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
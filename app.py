from flask import Flask, redirect, render_template, url_for
from flask_babel import Babel, gettext as _
    
app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'

langue='fr'
def get_locale():
    # Utilise la langue choisie par l'utilisateur (stockée en session)
    return langue

babel = Babel(app, locale_selector=get_locale)



@app.route('/')
def index():
    # Exemple de données pour les projets
    projects = [
        {
            'name': 'E-commerce Platform Redesign',
            'description': 'A complete UX/UI overhaul for an online retail client, boosting conversion rates by 15%.',
            'image': '/static/images/ecommerce.jpg',
            'tags': ['React', 'Figma', 'Node.js']
        }
    ]
    
    return render_template('index.html', projects=projects)

@app.route('/switchlanguage')
def switchlanguage():
    global langue
    langue = 'en' if langue == 'fr' else 'fr'
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
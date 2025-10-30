from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
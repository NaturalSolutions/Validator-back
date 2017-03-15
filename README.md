# restFulFlask
Création d'une API REST

#creation d'environement python3
mkdir appRestFulFlask
cd appRestFulFlask
export VENV=~/appRestFulFlask/env
python3 -m venv $VENV
source env/bin/activate

#installation
postgres doit etre installé
pip3 install flask
pip3 install psycopg2
pip3 install Flask-SQLAlchemy
pip3 install flask_script
pip3 install flask_migrate
pip3 install flask_cors

#configuration
- Modifier le fichier de configuration pour accéder à la base de données :
>cp config.cfg.default config.cfg

- Créer une base de données vide
- Ajouter vos paramètres de connexion à la base de données :
config.cfg : changer l'accès à la base de données
- l'application se charge de créer les tables

#lancer l'application
python3 app.py

#tester l'application
Ensemble (GET)
http http://127.0.0.1:5000/api/pois

Individu (GET)
http http://127.0.0.1:5000/api/pois/1

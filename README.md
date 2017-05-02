# Validator-back
Création d'une API REST pour une plateforme de validation de données
environnement :
* python 3
* Flask
* postgreSQL

## Création d'un environement python3 
Flask [http://flask.pocoo.org/docs/0.12/installation/]
- Cloner le dépôt
> git clone https://github.com/NaturalSolutions/Validator-back.git

> cd Validator-back

- Installer Virtualvenv
> sudo pip3 install virtualenv

- Créer un environnement python3
> . venv/bin/activate

## Installation des dépendances
postgreSQL doit être installé
* > pip3 install flask
* > pip3 install psycopg2
* > pip3 install Flask-SQLAlchemy
* > pip3 install flask_script
* > pip3 install flask_migrate
* > pip3 install flask_cors

## Configuration
- Modifier le fichier de configuration pour accéder à la base de données :
> cp config.cfg.default config.cfg

- Créer une base de données vide
- Ajouter vos paramètres de connexion à la base de données :
config.cfg : changer l'accès à la base de données
- l'application se charge de créer les tables

## Lancer l'application
python3 app.py

## Tester l'application
Ensemble (GET)
http http://127.0.0.1:5000/api/pois

Individu (GET)
http http://127.0.0.1:5000/api/pois/1

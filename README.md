# restFulFlask
Création d'une API REST

#creation d'environement python3 pour Flask [http://flask.pocoo.org/docs/0.12/installation/]
-213.80.Cloner le dépôt
> git clone 
> cd Validator-back

-Installer Virtualvenv
> sudo pip3 install virtualenv

-Créer un environnement python3
> . venv/bin/activate

#installation
postgres doit etre installé
> pip3 install flask
> pip3 install psycopg2
> pip3 install Flask-SQLAlchemy
> pip3 install flask_script
> pip3 install flask_migrate
> pip3 install flask_cors

#configuration
- Modifier le fichier de configuration pour accéder à la base de données :
> cp config.cfg.default config.cfg

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

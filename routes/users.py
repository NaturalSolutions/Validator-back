from flask import Flask, request, jsonify
from .__init__ import routes
import models
from app import db

@routes.route('/api/users', methods=['GET'])
def returnAllUsers():
    allUsers = models.Users.query.all()

    malist = []
    tempUser = 0
    for usr in allUsers:
        oneUser = models.Users.query.filter_by(id=usr.id).first()
        if(tempUser!=oneUser):
            tempUser=oneUser
            malist.append({'id': oneUser.id, 'last_name': oneUser.lastname, 'first_name': oneUser.firstname, 'email': oneUser.email, 'picture': oneUser.picture})
        oneCategorie = models.Categories.query.filter_by(id = usr.categories_id).first()
        malist.append({'role': oneCategorie.name})

    #creation d'un format approprié en utilisant le dictionnaire
    malistFormatBon=[] #format ideal
    dictionnaire={}
    compteurUser=0;
    compteur=2
    for i in range(len(malist)):
        for cle, valeur in malist[i].items():
            if(cle=='id'):
                compteurUser+=1;
            if(compteur==compteurUser):
                malistFormatBon.append(dictionnaire)
                dictionnaire={}
                compteur+=1
            dictionnaire[cle]=valeur
    malistFormatBon.append(dictionnaire)
    return jsonify({'users': malistFormatBon})


@routes.route('/api/users/<int:idu>', methods=['GET'])
def returnOneUser(idu):
    allUsers = models.Users.query.filter_by(id = idu).all()

    malist = []
    tempUser = 0
    for usr in allUsers:
        oneUser = models.Users.query.filter_by(id=usr.id).first()
        if(tempUser!=oneUser):
            tempUser=oneUser
            malist.append({'id': oneUser.id, 'last_name': oneUser.lastname, 'first_name': oneUser.firstname, 'email': oneUser.email, 'picture': oneUser.picture})
        oneCategorie = models.Categories.query.filter_by(id = usr.categories_id).first()
        malist.append({'role': oneCategorie.name})

    #creation d'un format approprié en utilisant le dictionnaire
    malistFormatBon=[] #format ideal
    dictionnaire={}
    compteurUser=0;
    compteur=2
    for i in range(len(malist)):
        for cle, valeur in malist[i].items():
            if(cle=='id'):
                compteurUser+=1;
            if(compteur==compteurUser):
                malistFormatBon.append(dictionnaire)
                dictionnaire={}
                compteur+=1
            dictionnaire[cle]=valeur
    malistFormatBon.append(dictionnaire)
    return jsonify({'user': malistFormatBon})





@routes.route('/api/users', methods=['POST'])
def addOneUser():

    try:
        userExist = models.Users.query.filter(models.Users.lastname==request.json['lastname']).filter(models.Users.firstname==request.json['firstname'])\
                                            .filter(models.Users.email==request.json['email']).first()

        if(userExist==None):
            newUser = models.Users(lastname=request.json['lastname'], firstname=request.json['firstname'], email=request.json['email'], categories_id=request.json['categories_id'])
            db.session.add(newUser)
        
            db.session.commit()

        return jsonify({'User': newUser.id}), 201;
        
    except:
        resp = jsonify({"error": 'Missing required fields'})
        resp.status_code = 403
        return resp

# lancer requete post : http  POST http://localhost:5000/api/users lastname=thom firstname=sand email=stho@gmail.com



@routes.route('/api/users', methods=['PATCH'])
def modifyOneUserValue():
    id_value = request.json['id']
    currentUser = models.Users.query.filter_by(id=id_value).first()

    for key, value in request.json.items():
        if key not in ['id']:
            if key in ['lastname']:
                currentUser.lastname = value
                db.session.commit()
            if key in ['firstname']:
                currentUser.firstname = value
                db.session.commit()
            if key in ['email']:
                currentUser.email = value
                db.session.commit()
            if key in ['picture']:
                currentUser.picture = value
                db.session.commit()
            if key in ['categorie_id']:
                currentUser.categorie_id = value
                db.session.commit()
            if key in ['accounts_id']:
                currentUser.accounts_id = value
                db.session.commit()

    return jsonify({'User': currentUser.id}), 204

# lancer requete patch : http  PATCH http://localhost:5000/api/users id=2 lastname=cape firstname=elo



@routes.route('/api/users/<int:idu>', methods=['DELETE'])
def deleteOneUser(idu):
    currentUser = models.Users.query.filter_by(id=idu).first()
    db.session.delete(currentUser)
    db.session.commit()
    
    return "SUPPR. OK", 200

# lancer requete delete : http  DELETE http://localhost:5000/api/users/2


            


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
            malist.append({'id': oneUser.id, 'lastname': oneUser.lastname, 'firstname': oneUser.firstname, 'email': oneUser.email, 'picture': oneUser.picture})
        oneCategorie = models.Categories.query.filter_by(id = usr.categories_id).first()
        malist.append({'role': oneCategorie.name})

    #creation d'un format approprié en utilisant le dictionnaire
    malistFormatBon=[] 
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
    return jsonify({'users': malistFormatBon}), 200


@routes.route('/api/users/<int:idu>', methods=['GET'])
def returnOneUser(idu):
    allUsers = models.Users.query.filter_by(id = idu).all()

    malist = []
    tempUser = 0
    for usr in allUsers:
        oneUser = models.Users.query.filter_by(id=usr.id).first()
        if(tempUser!=oneUser):
            tempUser=oneUser
            malist.append({'id': oneUser.id, 'lastname': oneUser.lastname, 'firstname': oneUser.firstname, 'email': oneUser.email, 'picture': oneUser.picture})
        oneCategorie = models.Categories.query.filter_by(id = usr.categories_id).first()
        malist.append({'role': oneCategorie.name})

    #creation d'un format approprié en utilisant le dictionnaire
    malistFormatBon=[] 
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
    return jsonify({'user': malistFormatBon}), 200


@routes.route('/api/users', methods=['POST'])
def addOneUser():
	try:
	    userExist = models.Users.query.filter(models.Users.email==request.json['email']).first()
	except KeyError:
		return jsonify({"error": 'Key-name email is not found'})
	    

	if(userExist==None):
	    try:
	        newUser = models.Users(lastname=request.json['lastname'], firstname=request.json['firstname'], email=request.json['email'], categories_id=request.json['categories_id'])
	        db.session.add(newUser)
	        db.session.commit()
	    except KeyError:
	        resp = jsonify({"error": 'Missing required fields OR Wrong name key of one or more field(s)'})
	        resp.status_code = 403
	        return resp
	    return jsonify({'User': newUser.id}), 201
        
	else:
	    return jsonify({'Error': "E-mail already exists"}), 404
        
    

# lancer requete post : http  POST http://localhost:5000/api/users lastname=thom firstname=sand email=stho@gmail.com



@routes.route('/api/users/<int:idu>', methods=['PATCH'])
def modifyOneUserValue(idu):
    if(request.json is None):
    	return returnOneUser(idu)

    else:
	    currentUser = models.Users.query.filter_by(id=idu).first()
	    try:
	        for key, value in request.json.items():
	            if key in ['lastname']:
	                currentUser.lastname = value
	                db.session.commit()
	            elif key in ['firstname']:
	                currentUser.firstname = value
	                db.session.commit()
	            elif key in ['email']:
	                currentUser.email = value
	                db.session.commit()
	            elif key in ['picture']:
	                currentUser.picture = value
	                db.session.commit()
	            elif key in ['categorie_id']:
	                currentUser.categorie_id = value
	                db.session.commit()
	            elif key in ['accounts_id']:
	                currentUser.accounts_id = value
	                db.session.commit()
	            else :
	                raise KeyError("Error : wrong name field")
	        newUser = models.Users.query.filter_by(id=idu).first()

	        return jsonify({'User': currentUser.id, 'firstname': newUser.firstname, 'lastname': newUser.lastname, 'email': newUser.email, \
	                    'picture': newUser.picture, 'role': newUser.categories_id}), 200
	    except KeyError:
	        resp = jsonify({"error": 'Error : wrong name key of one or more field(s)'})
	        resp.status_code = 403
	        return resp

# lancer requete patch : http PATCH http://localhost:5000/api/users/2 lastname=cape firstname=elo categories_id=3



@routes.route('/api/users/<int:idu>', methods=['DELETE'])
def deleteOneUser(idu):

    currentUser = models.Users.query.filter_by(id=idu).first()

    if(currentUser is not None):
        db.session.delete(currentUser)
        db.session.commit()
        
        return "SUPPR. OK", 204
    else:
        return jsonify({"error": 'This user does not exists'}), 404

# lancer requete delete : http  DELETE http://localhost:5000/api/users/2


            


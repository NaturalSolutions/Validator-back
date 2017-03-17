from flask import Flask, request, jsonify
from .__init__ import routes
import models # par defaut python cherche dans le dossier d'où est lancer le script d'entrée
from app import db


@routes.route('/api/pois', methods=['GET'])
def returnAllPois():
	allAsso = models.Contributions.query.all()

	malist = []
	tempPoi=0
	tempField=0
	tempValue=0
	for ass in allAsso:
		onePoi = models.Pois.query.filter_by(id=ass.idpoi).first()
		if(tempPoi!=onePoi):
			tempPoi=onePoi
			malist.append({'id': onePoi.id, 'tour_id': onePoi.tour_id})

		oneField = models.Fields.query.filter_by(id=ass.idfield).first()
		if(tempField!=oneField):
			tempField=oneField

			oneValue = models.Values.query.filter_by(id=ass.idvalue).first()
			if(tempValue!=oneValue):
				tempValue=oneValue
				if(oneField.name != 'description'):
					malist.append({oneField.name : oneValue.value})

    #creation d'un format approprié en utilisant le dictionnaire
	malistFormatBon=[]
	dictionnaire={}
	compteurPoi=0;
	compteur=2
	for i in range(len(malist)):
		for cle, valeur in malist[i].items():
			if(cle=='id'):
				compteurPoi+=1;
			if(compteur==compteurPoi):
				malistFormatBon.append(dictionnaire)
				dictionnaire={}
				compteur+=1
			dictionnaire[cle]=valeur
	malistFormatBon.append(dictionnaire)
	return jsonify({'pois': malistFormatBon})



@routes.route('/api/pois/<int:idp>', methods=['GET'])
def returnOnepoi(idp):
	allAsso = models.Contributions.query.filter_by(idpoi=idp).all()

	malist = []
	tempPoi=0
	tempField=0
	tempValue=0
	for ass in allAsso:
		onePoi = models.Pois.query.filter_by(id = ass.idpoi).first()
		if(tempPoi!=onePoi):
			tempPoi=onePoi
			malist.append({'id': onePoi.id, 'tour_id': onePoi.tour_id})

		oneField = models.Fields.query.filter_by(id=ass.idfield).first()
		if(tempField!=oneField):
			tempField=oneField
			oneValue = models.Values.query.filter_by(id=ass.idvalue).first()
			if(tempValue!=oneValue):
				tempValue=oneValue
				malist.append({oneField.name : oneValue.value})

    #creation d'un format approprié en utilisant le dictionnaire
	malistFormatBon=[]
	dictionnaire={}
	compteurPoi=0;
	compteur=2
	for i in range(len(malist)):
		for cle, valeur in malist[i].items():
			if(cle=='idPoi'):
				compteurPoi+=1;
			if(compteur==compteurPoi):
				malistFormatBon.append(dictionnaire)
				dictionnaire={}
				compteur+=1
			dictionnaire[cle]=valeur
	malistFormatBon.append(dictionnaire)
	return jsonify({'poi': malistFormatBon})

@routes.route('/api/pois', methods=['POST'])
def addOnePoi():
    colRequired = models.Pois.getColRequired()
    colOptional = models.Pois.getColOptional()
    requiredVal = {}
    optionalVal = {}
    nbFind = 0
    nbToFind = len(colRequired)

    requiredVal['tour_id'] = request.json['tour_id']
    requiredVal['typespois_id'] = request.json['typespois_id']

    optionalVal['version'] = 1

    currentPoi = models.Pois(requiredVal, optionalVal)

    # currentPoi = models.Pois(tour_id=request.json['tour_id'],
    # typespois_id=request.json['typespois_id']) #id de la base extérieure qui
    # crée les itinéraires
    for key, value in request.json.items():
        if key not in ['tour_id', 'typespois_id']:
            currentField = models.Fields(pos=1, name=key)
            currentValue = models.Values(value=value)
            currentasso = models.Contributions(
                currentPoi, currentField, currentValue)
            db.session.add(currentasso)
            db.session.commit()
    print(dir(currentPoi))
    return jsonify({'Poi': currentPoi.id}), 201

# lancer requete post : http  POST http://localhost:5000/api/pois
# typespois_id=1 tour_id=11 desc=tatapouetpouet

from . import routes
import models
from flask import Flask, request, jsonify

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
	malistFormatBon=[] #format ideal
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
	return jsonify({'pois': malistFormatBon})



@routes.route('/api/pois', methods=['POST'])
def addOnePoi():
    # p=Pois(version=request.json['version'], tour_id=request.json['tour_id'])
    # db.session.add(p)
    # db.session.commit()
    # allPois=Pois.query.all()
    # malist=[]
    # for poi in allPois:
    # 	malist.append({'idPoi' : poi.idPoi, 'version' : poi.version, 'tour_id' : poi.tour_id})
    # return jsonify({'pois' : malist})

    currentPoi = Pois(tour_id=request.json['tour_id'], version=1)
    for key, value in request.json.items():
        if key not in ['tour_id']:
            currentField = Fields(pos=1, nameField=key)
            currentValue = Values(fieldValues=value)
            currentasso = Contributions(
                currentPoi, currentField, currentValue)
            db.session.add(currentasso)
            db.session.commit()
    return jsonify({'Poi' : currentPoi.idPoi}), 201

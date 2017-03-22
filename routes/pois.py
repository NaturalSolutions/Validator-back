from flask import Flask, request, jsonify
from .__init__ import routes
import models  # par defaut python cherche dans le dossier d'où est lancer le script d'entrée
from app import db


@routes.route('/api/pois', methods=['GET'])
def returnAllPois():
    allAsso = models.Contributions.query.all()

    malist = []
    tempPoi = 0
    tempField = 0
    tempValue = 0
    for ass in allAsso:
        onePoi = models.Pois.query.filter_by(id=ass.idpoi).first()
        if(tempPoi != onePoi):
            tempPoi = onePoi
            malist.append({'id': onePoi.id, 'tour_id': onePoi.tour_id})

        oneField = models.Fields.query.filter_by(id=ass.idfield).first()
        if(tempField != oneField):
            tempField = oneField

            oneValue = models.Values.query.filter_by(id=ass.idvalue).first()
            if(tempValue != oneValue):
                tempValue = oneValue
                if(oneField.name != 'description'):
                    malist.append({oneField.name: oneValue.value})


    # creation d'un format approprié en utilisant le dictionnaire
    malistFormatBon = []
    dictionnaire = {}
    compteurPoi = 0
    compteur = 2
    for i in range(len(malist)):
        for cle, valeur in malist[i].items():
            if(cle == 'id'):
                compteurPoi += 1
            if(compteur == compteurPoi):
                malistFormatBon.append(dictionnaire)
                dictionnaire = {}
                compteur += 1
            dictionnaire[cle] = valeur
    malistFormatBon.append(dictionnaire)
    return jsonify({'pois': malistFormatBon}), 200


@routes.route('/api/pois/<int:idp>', methods=['GET'])
def returnOnepoi(idp):
    allAsso = models.Contributions.query.filter_by(idpoi=idp).all()

    malist = []
    tempPoi = 0
    tempField = 0
    tempValue = 0
    for ass in allAsso:
        onePoi = models.Pois.query.filter_by(id=ass.idpoi).first()
        if(tempPoi != onePoi):
            tempPoi = onePoi
            malist.append({'id': onePoi.id, 'tour_id': onePoi.tour_id})

        oneField = models.Fields.query.filter_by(id=ass.idfield).first()
        if(tempField != oneField):
            tempField = oneField
            oneValue = models.Values.query.filter_by(id=ass.idvalue).first()
            if(tempValue != oneValue):
                tempValue = oneValue
                malist.append({oneField.name: oneValue.value})


    # creation d'un format approprié en utilisant le dictionnaire
    malistFormatBon = []
    dictionnaire = {}
    compteurPoi = 0
    compteur = 2
    for i in range(len(malist)):
        for cle, valeur in malist[i].items():
            if(cle == 'idPoi'):
                compteurPoi += 1
            if(compteur == compteurPoi):
                malistFormatBon.append(dictionnaire)
                dictionnaire = {}
                compteur += 1
            dictionnaire[cle] = valeur
    malistFormatBon.append(dictionnaire)
    return jsonify({'poi': malistFormatBon}), 200


@routes.route('/api/pois', methods=['POST'])
def addOnePoi():
    colRequired = models.Pois.getColRequired()
    colOptional = models.Pois.getColOptional()
    requiredVal = {}
    optionalVal = {}
    nbFind = 0
    nbToFind = len(colRequired)
    fieldExist = 0
    rjson = request.get_json()
    tour_id = rjson.get("tour_id", "null")
    typespois_id = rjson.get("typespois_id", "null")

    if (tour_id != "null") :
        optionalVal['tour_id'] = request.json['tour_id']
    else:
        optionalVal['tour_id'] = 0
    try:
        if (typespois_id != "null") :
            requiredVal['typespois_id'] = request.json['typespois_id']
        else:
            raise ValueError("Error : Missing required field")

        currentPoi = models.Pois(requiredVal, optionalVal)
        for key, value in request.json.items():
            if key not in ['tour_id', 'typespois_id']:
                fieldExist = models.Fields.query.filter_by(name=key).first()
                if (fieldExist == None):
                    currentField = models.Fields(pos=1, name=key)
                else:
                    currentField = fieldExist
                currentValue = models.Values(value=value)
                currentasso = models.Contributions(1, 'in progress',
                                                   currentPoi, currentField, currentValue)
                db.session.add(currentasso)
                db.session.commit()
        return jsonify({'Poi': currentPoi.id}), 201
    except ValueError:
        resp = jsonify({"error": 'Missing required field'})
        resp.status_code = 403
        return resp

# lancer requete post : http  POST http://localhost:5000/api/pois typespois_id=1 tour_id=11 desc=tatapouetpouet



@routes.route('/api/pois/<int:idp>', methods=['PATCH'])
def modifyOnePoiFieldValue(idp):
    try:
        currentPoi = models.Pois.query.filter_by(id = idp).first()
        if(currentPoi == None):
            raise ValueError('This POI does not exist')
    except ValueError:
        resp = jsonify({"error": 'This POI does not exist'})
        resp.status_code = 404
        return resp

    if(request.json is None):
        return returnOnepoi(idp)

    try:
        contribExist = 0
        for key, value in request.json.items():
            currentField = models.Fields.query.filter_by(name=key).first()

            allContribs = models.Contributions.query.all()
            for contrib in allContribs:
                if(contrib.idpoi == currentPoi.id and contrib.idfield == currentField.id):
                    contribExist = 1;
                    lastContrib = contrib;

            if(contribExist):
                currentValue = models.Values(value=value)
                currentContrib = models.Contributions(lastContrib.version+1, 'in progress',
                                               currentPoi, currentField, currentValue)
                db.session.add(currentContrib)
            else:
                currentValue = models.Values(value=value)
                currentContrib = models.Contributions(1, 'in progress',
                                           currentPoi, currentField, currentValue)
                db.session.add(currentContrib)
        db.session.commit()

        return jsonify({'poi_id': currentPoi.id, 'field_id': currentField.id, 'field_name': currentField.name,\
                        'value_id': currentContrib.idvalue, 'value': value,  }), 200
    except:
        resp = jsonify({"error": 'Missing required fields or Bad key of entered name fields'})
        resp.status_code = 403
        return resp


# lancer requete patch : http PATCH http://localhost:5000/api/pois/110 desc=newValue




@routes.route('/api/pois/<int:idp>', methods=['DELETE'])
def deleteOnePoi(idp):

    selectedPoi = models.Pois.query.filter_by(id=idp).first()
    if(selectedPoi is not None):
        selectedContribs = models.Contributions.query.filter_by(idpoi=idp).all()

        for contrib in selectedContribs:
            selectedPoisValues = models.Values.query.filter_by(id=contrib.idvalue).first()
            db.session.delete(selectedPoisValues)

        db.session.commit()


        db.session.delete(selectedPoi)
        db.session.commit()

        for contribution in selectedContribs:
            db.session.delete(contribution)
        db.session.commit()


        return "SUPPR. OK", 204
    else:
        return jsonify({"error": 'This POI does not exists'}), 404

# lancer requete delete : http  DELETE http://localhost:5000/api/pois/110

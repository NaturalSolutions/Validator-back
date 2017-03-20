from flask import Flask, request, jsonify
from .__init__ import routes
import models
from app import db



@routes.route('/api/contributions', methods=['GET'])
def returnAllContributions():
    allAsso = models.Contributions.query.all()

    malist = []
    tempPoi=0
    tempField=0
    tempValue=0
    for ass in allAsso:

        oneValue = models.Values.query.filter_by(id=ass.idvalue).first()
        if(tempValue!=oneValue):
            tempValue=oneValue
            malist.append({'id': oneValue.id, 'created_date': oneValue.createddate, 'value': oneValue.value})

            oneUser = models.Values.query.filter_by(id=oneValue.users_id).first()
            theUser = models.Users.query.filter_by(id=oneUser.id).first()
            malist.append({'user_name': theUser.lastname})

        onePoi = models.Pois.query.filter_by(id=ass.idpoi).first()
        malist.append({'poi_id': onePoi.id})

        oneField = models.Fields.query.filter_by(id=ass.idfield).first()
        if(tempField!=oneField):
            tempField=oneField
            malist.append({'field_name' : oneField.name})

        malist.append({'status': ass.status, 'version': ass.version})

    #creation d'un format approprié en utilisant le dictionnaire
    malistFormatBon=[] 
    dictionnaire={}
    compteurContrib=0;
    compteur=2
    for i in range(len(malist)):
        for cle, valeur in malist[i].items():
            if(cle=='id'):
                compteurContrib+=1;
            if(compteur==compteurContrib):
                malistFormatBon.append(dictionnaire)
                dictionnaire={}
                compteur+=1
            dictionnaire[cle]=valeur
    malistFormatBon.append(dictionnaire)
    return jsonify({'contributions': malistFormatBon}), 200


@routes.route('/api/contributions/<int:idp>', methods=['GET'])
def returnContributionsByPoi(idp):
    allAsso = models.Contributions.query.filter_by(idpoi=idp).all()

    malist = []
    tempPoi=0
    tempField=0
    tempValue=0
    for ass in allAsso:

        oneValue = models.Values.query.filter_by(id=ass.idvalue).first()
        if(tempValue!=oneValue):
            tempValue=oneValue
            malist.append({'id': oneValue.id, 'created_date': oneValue.createddate, 'value': oneValue.value})

            oneUser = models.Fields.query.filter_by(id=oneValue.users_id).first()
            theUser = models.Users.query.filter_by(id=oneUser.id).first()
            malist.append({'user_name': theUser.lastname})

        onePoi = models.Pois.query.filter_by(id=ass.idpoi).first()
        malist.append({'poi_id': onePoi.id})

        oneField = models.Fields.query.filter_by(id=ass.idfield).first()
        if(tempField!=oneField):
            tempField=oneField
            malist.append({'field_name' : oneField.name})

        malist.append({'status': ass.status,  'version': ass.version})
        
    #creation d'un format approprié en utilisant le dictionnaire
    malistFormatBon=[] 
    dictionnaire={}
    compteurContrib=0;
    compteur=2
    for i in range(len(malist)):
        for cle, valeur in malist[i].items():
            if(cle=='id'):
                compteurContrib+=1;
            if(compteur==compteurContrib):
                malistFormatBon.append(dictionnaire)
                dictionnaire={}
                compteur+=1
            dictionnaire[cle]=valeur
    malistFormatBon.append(dictionnaire)
    return jsonify({'contributionsByPoi': malistFormatBon}), 200


def returnContributionsByIdvalue(idv):
    
    malist =[]

    selectedContrib = models.Contributions.query.filter_by(idvalue=idv).first()

    selectedValue = models.Values.query.filter_by(id=selectedContrib.idvalue).first()
    malist.append({'id': selectedValue.id, 'created_date': selectedValue.createddate, 'value': selectedValue.value})
    selectedUser = models.Users.query.filter_by(id=selectedValue.users_id).first()
    malist.append({'user_name': selectedUser.lastname})

    selectedPoi = models.Pois.query.filter_by(id=selectedContrib.idpoi).first()
    malist.append({'poi_id': selectedPoi.id})

    selectedField = models.Fields.query.filter_by(id=selectedContrib.idfield).first()
    malist.append({'field_name' : selectedField.name})

    return jsonify({'contributionsByIdvalue': malist})


@routes.route('/api/contributions/<int:idv>', methods=['PATCH'])
def modifyOneContributionStatus(idv):
    if(request.json is None):
        return returnContributionsByIdvalue(idv)
    else:
        try:
        	newStatus = request.json['status'];

        	selectedValue = models.Values.query.filter_by(id = idv).first()
        	idUser = selectedValue.users_id
        	selectedUser= models.Users.query.filter_by(id = idUser).first()

        	selectedContrib = models.Contributions.query.filter_by(idvalue = idv).first()
        	selectedContrib.status = newStatus
        	db.session.commit()

        	return jsonify({'status':selectedContrib.status, 'poi_id': selectedContrib.idpoi, \
        			'created_date': selectedValue.createddate,'field_id':selectedContrib.idfield , \
        			'value_id': selectedContrib.idvalue, 'user_name': selectedUser.lastname}), 200
        except:
            resp = jsonify({"error": 'Wrong patch on Contributions > only status can be patched'})
            resp.status_code = 403
            return resp


# lancer requete patch : http PATCH http://localhost:5000/api/contributions/990 status=updated



@routes.route('/api/contributions', methods=['DELETE'])
def deleteOneContribution():
    id_value =  request.json['idvalue'];

    selectedContrib = models.Contributions.query.filter_by(idvalue = id_value).first()

    if(selectedContrib is not None):
    	idpoiConcerned = selectedContrib.idpoi

    	selectedValue = models.Values.query.filter_by(id=id_value).first()
    	db.session.delete(selectedValue)
    	db.session.commit()

    	allContribPoiCount = models.Contributions.query.filter_by(idpoi=idpoiConcerned).count()
    	if(allContribPoiCount == 0):
    		associatedPoi = models.Pois.query.filter_by(id=idpoiConcerned).first()
    		db.session.delete(associatedPoi)
    	
    	db.session.delete(selectedContrib)
    	db.session.commit()


    	return "SUPPR. OK", 204
    else:
        return jsonify({"error": 'This idvalue does not exists'}), 404


# lancer requete delete : http DELETE  http://localhost:5000/api/contributions idvalue=1008









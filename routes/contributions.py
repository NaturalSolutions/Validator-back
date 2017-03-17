from flask import Flask, request, jsonify
from .__init__ import routes

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
    malistFormatBon=[] #format ideal
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
    return jsonify({'contributions': malistFormatBon})


@routes.route('/api/contributions/<int:idp>', methods=['GET'])
def returnContributionsById(idp):
    allAsso = models.Contributions.query.filter_by(idpoi=idp).all()

    malist = [] #format qui nous arrange pas
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
            malist.append({'field.name' : oneField.name})

        malist.append({'status': ass.status,  'version': ass.version})
        
    #creation d'un format approprié en utilisant le dictionnaire
    malistFormatBon=[] #format ideal
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
    return jsonify({'contributionsByPoi': malistFormatBon})

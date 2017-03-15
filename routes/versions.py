from . import routes
import models

'''@routes.route('/api/versions/poi/<int:idp>', methods=['GET'])
def returnVersionsOfOnePoi(idp):
    allAsso = models.Contributions.query.filter_by(idpoi=idp).all()

    malist = []
    tempPoi=0
    tempField=0
    tempValue=0
    tempVersion = 0
    for ass in allAsso:

        oneVersion = models.Contributions.query.filter_by(version=ass.version).first()
        #if(tempVersion!=oneVersion):
            #tempVersion=oneVersion
        malist.append({'version': oneVersion.version})

        onePoi = models.Pois.query.filter_by(id=ass.idpoi).first()
        #if(tempPoi!=onePoi):
            #tempPoi=onePoi
        malist.append({'id': onePoi.id, 'tour_id': onePoi.tour_id})

        oneField = models.Fields.query.filter_by(id=ass.idfield).first()
        if(tempField!=oneField):
            tempField=oneField
            oneValue = models.Fields.query.filter_by(id=ass.idvalue).first()
            if(tempValue!=oneValue):
                tempValue=oneValue
                malist.append({oneField.name : oneValue.value})



    #creation d'un format approprié en utilisant le dictionnaire
    malistFormatBon=[] #format ideal
    dictionnaire={}
    compteurVersion=0;
    compteur=2
    for i in range(len(malist)):
        for cle, valeur in malist[i].items():
            if(cle=='version'):
                compteurVersion+=1;
            if(compteur==compteurVersion):
                malistFormatBon.append(dictionnaire)
                dictionnaire={}
                compteur+=1
            dictionnaire[cle]=valeur
    malistFormatBon.append(dictionnaire)
    return jsonify({'versions': malistFormatBon})'''


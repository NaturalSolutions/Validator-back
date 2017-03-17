from flask import Flask, request, jsonify
from .__init__ import routes


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

import flask_sqlalchemy
from datetime import datetime
import json
from DataBaseConnector import configTables
from Campaign.Campaign import Campaign as Campaign
from _pytest.compat import NoneType

def insertarCampaignBD(CampaignReceived):
	#Insertamos la campaña
	configTables.BD.metadata.create_all(configTables.engine) #Se crea la BD (o no, dependiendo si se ejecutó antes).
	#Insertamos fecha inicio, fecha fin, email dueño, hashtags y mentions en la tabla Campaign de la BD:
	new_campaignBD=configTables.Campaign(startDate=(datetime.strftime((CampaignReceived.startDate),"%d %m %Y %X")), finDate=(datetime.strftime((CampaignReceived.finDate),"%d %m %Y %X")), email=(CampaignReceived.emailDueño), hashtags=(CampaignReceived.hashtags), mentions=(CampaignReceived.mentions))
	configTables.session.add(new_campaignBD)

	#Y finalmente las agregamos a la BD con estas 3 lineas:
	configTables.session.new
	configTables.session.dirty
	configTables.session.commit() #Para que los cambios se efectivicen en la BD
	return new_campaignBD.id

def eliminarCampaignBDxUser(email_user):
	#Pueden ser 1 o mas campañas asociadas a un usuario, para eliminar TODAS sin importar la fecha hacemos: configTables.session.query(configTables.Campaign).filter_by(email=email_user).delete() y configTables.session.commit()
	listaCampaigns = configTables.session.query(configTables.Campaign).filter_by(email=email_user).all()
	#Ahora tenemos que ver que cada una de estas campañas NO hayan iniciado (que fecha_inicio_campaign < 
	# fecha_actual). Para esto hay que recorrer la lista y eliminar las que SI iniciaron.
	for c in listaCampaigns:
		#Cada c es un: <Campaign(idC='1', startDate='28 11 2018 18:02:00', finDate='02 12 2018 19:26:22', email='test@gmail.com', hashtags='#test-#mock', mentions='@testCampaign-@mockOK')>
		#Y accedo a los atributos con c.atributo (el atributo está en la tabla Campaign dentro de configTables), osea asi: print (c.id)
		idCampaign = c.id
		campaignRetornada = retornarCampaignBD(idCampaign)
		fecha_inicio_campaign = campaignRetornada.startDate
		fecha_actual=datetime.now()
		if not (fecha_inicio_campaign < fecha_actual):
			eliminarCampaignBDxID(idCampaign)

def retornarCampaignsBDxEmail(user_email):
	campaignsBD = configTables.session.query(configTables.Campaign).filter_by(email=user_email).all()
	campaigns = []
	for cBD in campaignsBD:
		c = Campaign(cBD.id, cBD.email, cBD.hashtags, cBD.mentions, cBD.startDate, cBD.finDate)
		campaigns.append(c)
	return campaigns

def eliminarTweetsxIDC(idC):
	tweets = configTables.session.query(configTables.Tweet).filter_by(idCampaign=idC).all()
	for t in tweets:
		configTables.session.delete(t)
	configTables.session.commit()

def eliminarCampaignBDxID(idC):
	campaignespecifica = configTables.session.query(configTables.Campaign).get(idC) #Obtengo al campaña con id especifico idC.
	configTables.session.delete(campaignespecifica)
	configTables.session.commit()

def retornarCampaignBD(idC):
	campaignespecifica = configTables.session.query(configTables.Campaign).get(idC)
	#Con la campaignespecifica de arriba accedemos a los atributos así: (ya que es el objeto Campaign de configTables.py)
	#print(campaignespecifica.id, campaignespecifica.email, campaignespecifica.hashtags, campaignespecifica.mentions, campaignespecifica.startDate, campaignespecifica.finDate) 
    #Devuelve esto: 2 donaldTrump@gmail.com #federicio-#federicio2 @hola-@hola2 2018-11-28 2018-12-02 --> con print envés de return se ve.
	if type(campaignespecifica) == NoneType:
		return []
	return Campaign(campaignespecifica.id, campaignespecifica.email, campaignespecifica.hashtags, campaignespecifica.mentions, campaignespecifica.startDate, campaignespecifica.finDate)
	#Con el objetoCampaign de arriba accedemos a los atributos así: (ya que es el objeto Campaign de Campaign.py)
	#print(campaignespecifica.idC, campaignespecifica.emailDueño, campaignespecifica.hashtags, campaignespecifica.mentions, campaignespecifica.startDate, campaignespecifica.finDate) 


#Desde la Interfaz (en ModifCampaign) le llegaría al manager la columna a modificar, el campo para esa columna (inputUser) y el id de campaña.
def modificarCampaignBD(idC, inputColumn, inputUser):
	#Lenguaje MYSQL: UPDATE Campaign SET columna = "inputuser" WHERE id = "idC".
	campaignespecifica = configTables.session.query(configTables.Campaign).get(idC)
	#Hice esto de abajo porque no podía poner campaignespecifica.inputColumn = inputUser, no me toma inputColumn.
	wasModified = False 	#Flag que indica si fue modificado
	if (inputColumn=="email"):
		campaignespecifica.email = inputUser
		configTables.session.commit()
		wasModified = True
	
	if (inputColumn=="startDate"):
		campaignespecifica.startDate = inputUser
		configTables.session.commit()
		wasModified = True

	if (inputColumn=="finDate"):
		campaignespecifica.finDate = inputUser
		configTables.session.commit()
		wasModified = True

	if (inputColumn=="hashtags"):
		campaignespecifica.hashtags = listaAString(inputUser)
		configTables.session.commit()
		wasModified = True

	if (inputColumn=="mentions"):
		campaignespecifica.mentions = listaAString(inputUser)
		configTables.session.commit()
		wasModified = True
		
	return wasModified
	#print(campaignespecifica.id, campaignespecifica.email, campaignespecifica.hashtags, campaignespecifica.mentions, campaignespecifica.startDate, campaignespecifica.finDate) 

def insertTweet(TweetInput, idC):
	print (TweetInput.hashtags) 
	print (TweetInput.mentions) 
	configTables.BD.metadata.create_all(configTables.engine) #Se crea la BD (o no, dependiendo si se ejecutó antes).
	#Insertamos fecha publicacion, autor, mensaje y macheo en la tabla Tweet de la BD:
	stringHashtag = listaAString(TweetInput.hashtags) # #donaldTrump-#G20
	stringMention = listaAString(TweetInput.mentions) # @donaldTrump-@miauricioOK
	#print(TweetInput.ID, TweetInput.userName, TweetInput.userID, TweetInput.hashtags ,TweetInput.mentions, TweetInput.date)
	IDTweet=(TweetInput.ID)
	if returnTweetByIDT(IDTweet):
		print("Tweet ya ingresado")
	else:
		UserName=(TweetInput.userName).encode('ascii',errors='ignore') #Hacemos esto por si hay caracteres especiales o emoticonos en el nombre de usuario.
		new_TweetBD=configTables.Tweet(idCampaign=(idC), ID=(IDTweet), userName=(UserName), userid=(TweetInput.userID), hashtags=(stringHashtag),mentions=(stringMention), date=(TweetInput.date))
		configTables.session.add(new_TweetBD)
		#Y finalmente las agregamos a la BD con estas 3 lineas:
		configTables.session.new
		configTables.session.dirty
		configTables.session.commit()

def returnTweetByIDT(idT):
	tweetEspecifico = configTables.session.query(configTables.Tweet).get(idT)
	return tweetEspecifico

def returnTweetsByIDC(IDC):
	tweetsBD = configTables.session.query(configTables.Tweet).filter_by(idCampaign=IDC).all()
	#tweetsBD es una lista de Tweets en el formato de Tweet de ConfigTables: 
	#[<Tweets(ID='112112', userName='MiauricioOK',userid='451325',hashtags='#DonaldNoMeDejes',mentions='@donaldTrump-@G20',date='2018-03-20 21:08:01',idCampaign='3')>, 
	#<Tweets(ID='123456', userName='NASAOk',userid='789456',hashtags='#mars-#venus-#earth',mentions='@NASA-@planets',date='2018-03-20 15:11:01',idCampaign='3')>]

	#Tenemos que separar los tweets y crear objetos tweets. Y hacerles el to json. 
	#Y hacer una lista de esos to json. 
	tweets = []
	for t in tweetsBD:
		dictionary = {
        	"id_str" : t.ID,
        	"user" : {"name" : t.userName, "id_str" : t.userid},
        	"entities" : {"hashtags" : t.hashtags,"user_mentions" : t.mentions},
        	"created_at" : t.date,
    	}
		tweets.append(dictionary)
	return tweets

def listaAString(lista):
		string = "-".join(lista)
		return string
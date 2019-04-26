'''
Created on Dec 19, 2018

@author: Gabriel Torrandella
'''
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import relationship


engine = create_engine("sqlite:///:memory:")
if not database_exists(engine.url):
    create_database(engine.url)
#Este objeto va a contener la meta-informacion de nuestros mapeos:
BD = declarative_base()
#Este objeto session va a ser nuestro contrato con el ORM, va a ser el objeto por el cual nos vamos a comunicar:
Session = sessionmaker(bind=engine)
session = Session()

class Campaign(BD):
    __tablename__ = 'campaign'

    id = Column(Integer, primary_key=True)
    startDate = Column(String(30))
    finDate = Column(String(30))
    email = Column(String(30))
    hashtags = Column(String(50))
    mentions = Column(String(50))
    tuits = relationship("Tweet")

    def __repr__(self):
        return "<Campaign(idC='%s', startDate='%s', finDate='%s', email='%s', hashtags='%s', mentions='%s')>" % (self.id, self.startDate, self.finDate, self.email, self.hashtags, self.mentions)

class Tweet(BD):
    __tablename__ = 'tweets'
    
    ID = Column(Integer, primary_key=True)
    userName = Column(String(50))
    userid = Column(String(30))
    hashtags = Column(String(50))
    mentions = Column(String(50))
    date = Column(String(30))
    idCampaign = Column(Integer, ForeignKey('campaign.id'))

    def __repr__(self):
        return "<Tweets(ID='%s', userName='%s',userid='%s',hashtags='%s',mentions='%s',date='%s',idCampaign='%s')>" % (self.ID, self.userName, self.userid, self.hashtags, self.mentions, self.date, self.idCampaign)
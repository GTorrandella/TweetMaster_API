'''
Created on Dec 12, 2018

@author: Gabriel Torrandella
'''
import unittest

from DataBaseConnector import test_database
import DataBaseConnector.configTables as configTables

from Manager import manager_flask
from Manager.tests.test_manager_base import test_manager_base

from datetime import datetime
from flask import json


class test_manager_flask(test_manager_base):

    def databaseSetUp(self):
        configTables.engine = test_database.engine
        configTables.BD = test_database.BD
        configTables.session = test_database.session
        
        configTables.Campaign = test_database.Campaign
        configTables.Tweet = test_database.Tweet
        
        configTables.Campaign.metadata.create_all(configTables.engine)
        configTables.Tweet.metadata.create_all(configTables.engine)
        
        for c in self.initialCampaigns:
            configTables.session.add(configTables.Campaign(startDate=(datetime.strftime((c.startDate),"%d %m %Y %X")), finDate=(datetime.strftime((c.finDate),"%d %m %Y %X")), email=(c.emailDueño), hashtags=(c.hashtags), mentions=(c.mentions)))
        configTables.session.new
        configTables.session.dirty
        configTables.session.commit()
        


    def setUp(self):
        test_manager_base.setUp(self)
        
        self.databaseSetUp()
                
        self.test_app = manager_flask.app.test_client()

    def tearDown(self):
        
        configTables.BD.metadata.drop_all(configTables.engine)


    def test_POST_201(self):
        
        initialCampaignNumber = len(configTables.session.query(configTables.Campaign).all())
        self.assertEqual(initialCampaignNumber, 3)
        
        response = self.test_app.post('/Campaing', json = self.campaignCreationData, content_type='application/json')
        
        self.assertEqual(response.status, '201 CREATED')
        
        afterCampaigns = configTables.session.query(configTables.Campaign).all()
        newCampaign = afterCampaigns[3]
        
        self.assertEqual(len(afterCampaigns), 4)
        
        self.assertEqual(newCampaign.id, 4)
        self.assertEqual(newCampaign.email, 'hype@example.com')
        self.assertEqual(newCampaign.hashtags, '#JOKER-#SMASH')
        self.assertEqual(newCampaign.mentions, '@Sora_Sakurai')
        self.assertEqual(newCampaign.startDate, "31 12 2050 23:20:00")
        self.assertEqual(newCampaign.finDate, "01 01 2051 00:30:00")
                                 
    
    def test_POST_412(self):
        initialCampaignNumber = len(configTables.session.query(configTables.Campaign).all())
        self.assertEqual(initialCampaignNumber, 3)
        
        response = self.test_app.post('/Campaing', json = self.campaignCreationDataError, content_type='application/json')
        
        self.assertEqual(response.status, '412 PRECONDITION FAILED')
        
        afterCampaigns = configTables.session.query(configTables.Campaign).all()
        self.assertEqual(len(afterCampaigns), 3)

    def test_DELETE_by_id_200(self):
        initialCampaignNumber = len(configTables.session.query(configTables.Campaign).all())
        self.assertEqual(initialCampaignNumber, 3)
        
        response = self.test_app.delete('/Campaing', json = self.campaignDeleteByIDCData, content_type='application/json')
        
        self.assertEqual(response.status, '200 OK')
        
        afterCampaigns = configTables.session.query(configTables.Campaign).all()
        self.assertEqual(len(afterCampaigns), 2)
        self.assertFalse(1 in [afterCampaigns[0].id,afterCampaigns[1].id])
        
    def test_DELETE_by_email_200(self):
        initialCampaignNumber = len(configTables.session.query(configTables.Campaign).all())
        self.assertEqual(initialCampaignNumber, 3)
        
        response = self.test_app.delete('/Campaing', json = self.campaignDeleteByEmailData, content_type='application/json')
        
        self.assertEqual(response.status, '200 OK')
        
        afterCampaigns = configTables.session.query(configTables.Campaign).all()
        self.assertEqual(len(afterCampaigns), 2)
        self.assertFalse(2 in [afterCampaigns[0].id,afterCampaigns[1].id])
    
    def test_DELETE_412(self):
        initialCampaignNumber = len(configTables.session.query(configTables.Campaign).all())
        self.assertEqual(initialCampaignNumber, 3)
        
        response = self.test_app.delete('/Campaing', json = self.campaignDeleteDataError, content_type='application/json')
        
        self.assertEqual(response.status, '412 PRECONDITION FAILED')
        
        afterCampaigns = configTables.session.query(configTables.Campaign).all()
        self.assertEqual(len(afterCampaigns), 3)
    
    def test_GET_200(self):
        initialCampaignNumber = len(configTables.session.query(configTables.Campaign).all())
        self.assertEqual(initialCampaignNumber, 3)
        
        response = self.test_app.get('/Campaing/3')
        self.assertEqual(response.status, '200 OK')
        
        responseCampaign = json.loads(response.json)
        self.assertEqual(responseCampaign['id'], 3)
        self.assertEqual(responseCampaign['email'], 'c@example.com')
        self.assertEqual(responseCampaign['hashtags'], ['#nintendo','#SMASH'])
        self.assertEqual(responseCampaign['mentions'], ['@Sora_Sakurai','@nintendo'])
        self.assertEqual(responseCampaign['startDate'], "31 12 2050 23:20:00")
        self.assertEqual(responseCampaign['finDate'], "01 01 2051 00:30:00")
        
        afterCampaigns = configTables.session.query(configTables.Campaign).all()
        self.assertEqual(len(afterCampaigns), 3)
    
    def test_GET_404(self):
        initialCampaignNumber = len(configTables.session.query(configTables.Campaign).all())
        self.assertEqual(initialCampaignNumber, 3)
        
        response = self.test_app.get('/Campaing/8')
        self.assertEqual(response.status, '404 NOT FOUND')
    
    def test_PACTH_202(self):
        initialCampaign = configTables.session.query(configTables.Campaign).all()
        self.assertEqual(len(initialCampaign), 3)
        
        campaignToPatch = initialCampaign[2]
        self.assertEqual(campaignToPatch.id, 3)
        self.assertEqual(campaignToPatch.email, 'c@example.com')
        self.assertEqual(campaignToPatch.hashtags, '#nintendo-#SMASH')
        self.assertEqual(campaignToPatch.mentions, '@Sora_Sakurai-@nintendo')
        self.assertEqual(campaignToPatch.startDate, "31 12 2050 23:20:00")
        self.assertEqual(campaignToPatch.finDate, "01 01 2051 00:30:00")
        
        response = self.test_app.patch('/Campaing/3', json=self.campaignPatchHashtagsData, content_type='application/json')
        self.assertEqual(response.status, "202 ACCEPTED")
        
        patchedCampaigns = configTables.session.query(configTables.Campaign).all()
        self.assertEqual(len(patchedCampaigns), 3)
        
        patchedHashtagsCampaign = patchedCampaigns[2]
        self.assertEqual(patchedHashtagsCampaign.id, 3)
        self.assertEqual(patchedHashtagsCampaign.email, 'c@example.com')
        self.assertEqual(patchedHashtagsCampaign.hashtags, '#qatherine-#katherine-#catherine')
        self.assertEqual(patchedHashtagsCampaign.mentions, '@Sora_Sakurai-@nintendo')
        self.assertEqual(patchedHashtagsCampaign.startDate, "31 12 2050 23:20:00")
        self.assertEqual(patchedHashtagsCampaign.finDate, "01 01 2051 00:30:00")
        
        response = self.test_app.patch('/Campaing/3', json=self.campaignPatchMentionsData, content_type='application/json')
        self.assertEqual(response.status, "202 ACCEPTED")
        
        patchedCampaigns = configTables.session.query(configTables.Campaign).all()
        self.assertEqual(len(patchedCampaigns), 3)
        
        patchedHashtagsCampaign = patchedCampaigns[2]
        self.assertEqual(patchedHashtagsCampaign.id, 3)
        self.assertEqual(patchedHashtagsCampaign.email, 'c@example.com')
        self.assertEqual(patchedHashtagsCampaign.hashtags, '#qatherine-#katherine-#catherine')
        self.assertEqual(patchedHashtagsCampaign.mentions, '@atlususa-@stud_zero')
        self.assertEqual(patchedHashtagsCampaign.startDate, "31 12 2050 23:20:00")
        self.assertEqual(patchedHashtagsCampaign.finDate, "01 01 2051 00:30:00")
        
    def test_PACTH_404(self):
        initialCampaignNumber = len(configTables.session.query(configTables.Campaign).all())
        self.assertEqual(initialCampaignNumber, 3)
        
        response = self.test_app.patch('/Campaing/8', json=self.campaignPatchHashtagsData, content_type='application/json')
        self.assertEqual(response.status, '404 NOT FOUND')

    def test_PACTH_412(self):
        initialCampaignNumber = len(configTables.session.query(configTables.Campaign).all())
        self.assertEqual(initialCampaignNumber, 3)
        
        response = self.test_app.patch('/Campaing/3', json=self.campaignPatchErrorData, content_type='application/json')
        self.assertEqual(response.status, '412 PRECONDITION FAILED')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
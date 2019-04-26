'''
Created on Dec 12, 2018

@author: Gabriel Torrandella
'''
import unittest

from Campaign.Campaign import Campaign


class test_manager_base(unittest.TestCase):

    
    campaignCreationData = {'email':'hype@example.com', 
                                 'hashtags':['#JOKER','#SMASH'], 
                                 'mentions':['@Sora_Sakurai'],
                                 'startDate':"31 12 2050 23:20:00",
                                 'endDate':"01 01 2051 00:30:00"}
    
    campaignCreationDataError = {'hashtags':'#JOKER-#smash', 
                                 'mentions':'@Sora_Sakurai',
                                 'startDate':"31 12 2050 23:20:00",
                                 'endDate':"01 01 2051 00:30:00"}
    
    campaignDeleteByIDCData = {'idC':1}
    campaignDeleteByEmailData = {'email':"b@example.com"}
    campaignDeleteDataError = {'hype':"JOKER_IN_SMASH"}
    
    campaignPatchHashtagsData = {'columnaAModif':'hashtags',
                                'campoColumna':['#qatherine','#katherine','#catherine']}
    
    campaignPatchMentionsData = {'columnaAModif':'mentions',
                                'campoColumna':['@atlususa','@stud_zero']}
    
    campaignPatchErrorData = {'campoColumna':['@atlususa','@stud_zero']}


    initialCampaigns = [Campaign(1, "a@example.com", '#NothingBreaksLikeAHeart', "", "31 12 2050 23:20:00", "01 01 2051 00:30:00"),
                        Campaign(2, "b@example.com", "", '@POTUS', "31 12 2050 23:20:00", "01 01 2051 00:30:00"),
                        Campaign(3, "c@example.com", '#nintendo-#SMASH', '@Sora_Sakurai-@nintendo', "31 12 2050 23:20:00", "01 01 2051 00:30:00")]
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
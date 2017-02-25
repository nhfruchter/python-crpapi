""" 
	Python library for interacting with the CRP API.

    The CRP API (https://www.opensecrets.org/api) provides campaign 
	finance and other data from the Center for Responsive Politics.

	See README.md for methods and usage
"""

__author__ = "James Turk (jturk@sunlightfoundation.com); forked by Nathaniel Fruchter (fruchter@mit.edu)"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2009 Sunlight Labs"
__license__ = "BSD"

import requests, requests.exceptions
try:
    import json
except ImportError:
    import simplejson as json

class CRPApiError(Exception):
    """ Exception for CRP API errors """

# results #
class CRPApiObject(object):
    def __init__(self, d):
        self.__dict__ = d

# namespaces #

class CRPApi(object):

    SUPPORTED_OUTPUTS = set(['json', 'xml', 'doc'])
    
    def __init__(self, apikey, output='json'):
        self.apikey = apikey
        
        if output not in self.SUPPORTED_OUTPUTS:
            raise ValueError("output must be one of %s" % self.SUPPORTED_OUTPUTS)
        else:    
            self.output = output
            
    def _apicall(self, func, params):
        """Do an API call against the OpenSecrets.org API. 
        
        :func = API call
            see :https://www.opensecrets.org/api/admin/index.php?function=user_api_list
        :params = parameters passed to API function call
        """

        baseURL = 'http://www.opensecrets.org/api/'
        
        # Set output format
        apicall = {
            'method': func,
            'apikey': self.apikey,
            'output': self.output
        }
        apicall.update(params)
        
        try:
            response = requests.get(baseURL, params=apicall)
            if self.output == 'json':                
                return json.loads(response.content)['response']
            else:
                return output    
        except requests.exceptions.RequestException as e:
            raise e
        except (ValueError, KeyError) as e:
            raise CRPApiError('Unable to parse invalid response from the API')        

    def getLegislators(self, **kwargs):
        """
        Provides a list of Congressional legislators and associated attributes for 
        specified subset (state, district or specific CID).
        
        parameters
            :value two character state code, or 4 character district or specific CID
        
        """
        results = self._apicall('getLegislators', kwargs)['legislator']
        return results

    def memPFDprofile(self, **kwargs):
        """
        Returns PFD (financial disclosure) information for a member of Congress

        parameters
            :cid CRP candidate ID
            :year Disclosure year (starting 2013)
        """
        
        results = self._apicall('memPFDprofile', kwargs)['member_profile']
        return results

    def candSummary(self, **kwargs):
        """
        Method to access summary data for a candidate
        
        parameters
            :cid CRP candidate ID
            :cycle Blank for current, or 2012, 2014, 2016.
            
        """        
        result = self._apicall('candSummary', kwargs)['summary']
        return result['@attributes']

    def candContrib(self, **kwargs):
        """
        Returns top contributors to specified candidate for a House or Senate seat or member of Congress. 
        These are 6 year numbers for Senators/Senate candidates; 2 years for Representatives/House candidates	
        
        parameters
            :cid CRP candidate ID
            :cycle Blank for current, or 2012, 2014, 2016.
        
        """
        results = self._apicall('candContrib', kwargs)['contributors']['contributor']
        return results

    def candIndustry(self, **kwargs):
        """
        Returns data on a candidate's Industry contributions to specified candidate for a House or Senate seat or member of Congress. 
        These are 6 year numbers for Senators/Senate candidates; 2 years for Representatives/House candidates
        
        parameters
            :cid CRP candidate ID
            :cycle Blank for current, or 2012, 2014, 2016.
        """
        results = self._apicall('candIndustry', kwargs)['industries']['industry']
        return results

    def candSector(self, **kwargs):
        """
        Provides sector total of specified politician's receipts
        
        parameters
            :cid CRP candidate ID
            :cycle Blank for current, or 2012, 2014, 2016.
        """
        results = self._apicall('candSector', kwargs)['sectors']['sector']
        return results

    def candIndByInd(self, **kwargs):
        """
        provides total contributed to specified candidate from specified industry for specified cycle

        parameters
            :cid CRP candidate ID
            :cycle Blank for current, or 2012, 2014, 2016.
            :ind 3 character industry code
        """
        result = self._apicall('CandIndByInd', kwargs)['candIndus']
        return result['@attributes']

    def getOrgs(self, **kwargs):
        """
        Search information about organization(s)
        
        parameters
            :org name or partial name of organization requested        
        """
        results = self._apicall('getOrgs', kwargs)['organization']
        return results
            
    def orgSummary(self, **kwargs):
        """
        Summary of information about an organization
        
        parameters
            :id A specific CRP orgid 
        """
        results = self._apicall('orgSummary', kwargs)['organization']
        return results
            
    def congCmteIndus(self, **kwargs):
        """
        Provides summary fundraising information for a specific committee, industry and congress number

        parameters
            :cmte Committee ID in CQ format
            :congno Congress session number (112, 113, 114, or blank for latest)
            :indus 3 character industry code
        """
        results = self._apicall('congCmteIndus', kwargs)['committee']['member']
        return results
        
    def independentExpend(self, **kwargs):
        """
        Return the 50 latest independent expenditures, updated daily.
        
        No parameters.
        """
        results = self._apicall('independentExpend', kwargs)
        return results

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
        results = self._apicall('getLegislators', kwargs)['legislator']
        return results

    def memPFDprofile(self, **kwargs):
        results = self._apicall('memPFDprofile', kwargs)['member_profile']
        return results

    def candSummary(self, **kwargs):        
        result = self._apicall('candSummary', kwargs)['summary']
        return result['@attributes']

    def candContrib(self, **kwargs):
        results = self._apicall('candContrib', kwargs)['contributors']['contributor']
        return results

    def candIndustry(self, **kwargs):
        results = self._apicall('candIndustry', kwargs)['industries']['industry']
        return results

    def candSector(self, **kwargs):
        results = self._apicall('candSector', kwargs)['sectors']['sector']
        return results

    def candIndByInd(self, **kwargs):
        result = self._apicall('CandIndByInd', kwargs)['candIndus']
        return result['@attributes']

    def getOrgs(self, **kwargs):
        results = self._apicall('getOrgs', kwargs)['organization']
        return results
            
    def orgSummary(self, **kwargs):
        results = self._apicall('orgSummary', kwargs)['organization']
        return results
            
    def congCmteIndus(self, **kwargs):
        results = self._apicall('congCmteIndus', kwargs)['committee']['member']
        return results
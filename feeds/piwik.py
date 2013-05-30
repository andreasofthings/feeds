#ToDo: rename to stats or somethign


# http://andreas.neumeier.org/piwik/?module=API&method=getDefaultMetrics&segment=pageUrl==/node/3&format=json&idSite=10&token_auth=9ac687241bcc056c6c4d62ebbcc48d3e
# http://andreas.neumeier.org/piwik/?module=API&method=VisitsSummary.getVisits&segment=pageUrl==/node/7/&format=json&idSite=10&period=week&date=today&token_auth=9ac687240bcc056c6c4d62ebbcc48d3e


import httplib2
import urlparse
import urllib, urllib2

from django.conf import settings 

try:
  from django.utils import simplejson
except:
  import simplejson

class Piwik:
  server = ""
  siteid = ""
  token_auth = ""

  available_methods = (
    'VisitsSummary.getVisits',
    'API.getDefaultMetrics', # () [ Example in [42]XML, [43]Json, [44]Tsv
    'API.getDefaultProcessedMetrics', # () [ Example in [45]XML, [46]Json,
    'API.getDefaultMetricsDocumentation', # () [ Example in [48]XML, [49]Json,
    'API.getSegmentsMetadata', # (idSites = 'Array') [ Example in [51]XML,
    'API.getVisitEcommerceStatusFromId', # (id) [ No example available ]
    'API.getVisitEcommerceStatus', #  (status) [ No example available ]
    'API.getLogoUrl', #  (pathOnly = '') [ Example in [54]XML, [55]Json,
    'API.getHeaderLogoUrl', #  (pathOnly = '') [ Example in [57]XML, [58]Json,
    'API.getMetadata', #  (idSite, apiModule, apiAction, apiParameters =
    'API.getReportMetadata', #  (idSites = '', period = '', date = '') [
    'API.getProcessedReport', #  (idSite, period, date, apiModule, apiAction,
    'Actions.getPageUrls', #  (idSite, period, date, segment = '', expanded =
    'Actions.getPageUrl', #  (pageUrl, idSite, period, date, segment = '') [ No
    'Actions.getPageTitles', #  (idSite, period, date, segment = '', expanded =
    'Actions.getPageTitle', #  (pageName, idSite, period, date, segment = '') [
    'Actions.getDownloads', #  (idSite, period, date, segment = '', expanded =
    'Actions.getDownload', #  (downloadUrl, idSite, period, date, segment = '')
    'Actions.getOutlinks', #  (idSite, period, date, segment = '', expanded =
    'Actions.getOutlink', #  (outlinkUrl, idSite, period, date, segment = '') [
    'CustomVariables.getCustomVariables', #  (idSite, period, date, segment =
    'CustomVariables.getCustomVariablesValuesFromNameId', #  (idSite, period,
    'ExampleAPI.getPiwikVersion', #  () [ Example in [95]XML, [96]Json, [97]Tsv
    'ExampleAPI.getAnswerToLife', #  () [ Example in [98]XML, [99]Json,
    'ExampleAPI.getObject', #  () [ Example in [101]XML, [102]Json, [103]Tsv
    'ExampleAPI.getSum', #  (a = '0', b = '0') [ Example in [104]XML,
    'ExampleAPI.getNull', #  () [ Example in [107]XML, [108]Json, [109]Tsv
    'ExampleAPI.getDescriptionArray', #  () [ Example in [110]XML, [111]Json,
    'ExampleAPI.getCompetitionDatatable', #  () [ Example in [113]XML,
    'ExampleAPI.getMoreInformationAnswerToLife', #  () [ Example in [116]XML,
    'ExampleAPI.getMultiArray', #  () [ Example in [119]XML, [120]Json,
    'Goals.getGoals', #  (idSite) [ Example in [124]XML, [125]Json, [126]Tsv
    'Goals.addGoal', #  (idSite, name, matchAttribute, pattern, patternType,
    'Goals.updateGoal', #  (idSite, idGoal, name, matchAttribute, pattern,
    'Goals.deleteGoal', # (idSite, idGoal) [ No example available ]
    'Goals.getItemsSku', #  (idSite, period, date, abandonedCarts = '') [
    'Goals.getItemsName', #  (idSite, period, date, abandonedCarts = '') [
    'Goals.getItemsCategory', #  (idSite, period, date, abandonedCarts = '') [
    'Goals.get', #  (idSite, period, date, segment = '', idGoal = '', columns =
    'ImageGraph.get', #  (idSite, period, date, apiModule, apiAction, graphType
    'LanguagesManager.isLanguageAvailable', #  (languageCode) [ Example in
    'LanguagesManager.getAvailableLanguages', #  () [ Example in [151]XML,
    'LanguagesManager.getAvailableLanguagesInfo', #  () [ Example in [154]XML,
    'LanguagesManager.getAvailableLanguageNames', #  () [ Example in [157]XML,
    'LanguagesManager.getTranslationsForLanguage', #  (languageCode) [ Example
    'LanguagesManager.getLanguageForUser', #  (login) [ No example available ]
'LanguagesManager.setLanguageForUser', #  (login, languageCode) [ No
'Live.getCounters', #  (idSite, lastMinutes, segment = '') [ Example in
'Live.getLastVisitsDetails', #  (idSite, period = '', date = '', segment =
'PDFReports.addReport', #  (idSite, description, period, reportFormat,
'PDFReports.updateReport', #  (idReport, idSite, description, period,
'PDFReports.deleteReport', #  (idReport) [ No example available ]
'PDFReports.getReports', #  (idSite = '', period = '', idReport = '',
'PDFReports.generateReport', #  (idReport, date, idSite = '', language =
'PDFReports.sendEmailReport', #  (idReport, idSite, period = '', date = '')
'Provider.getProvider', #  (idSite, period, date, segment = '') [ Example
'Referers.getRefererType', #  (idSite, period, date, segment = '',
'Referers.getKeywords', #  (idSite, period, date, segment = '', expanded =
'Referers.getKeywordsForPageUrl', #  (idSite, period, date, url) [ Example
'Referers.getKeywordsForPageTitle', #  (idSite, period, date, title) [ No
'Referers.getSearchEnginesFromKeywordId', #  (idSite, period, date,
'Referers.getSearchEngines', #  (idSite, period, date, segment = '',
'Referers.getKeywordsFromSearchEngineId', #  (idSite, period, date,
'Referers.getCampaigns', #  (idSite, period, date, segment = '', expanded =
'Referers.getKeywordsFromCampaignId', #  (idSite, period, date, idSubtable,
'Referers.getWebsites', #  (idSite, period, date, segment = '', expanded =
'Referers.getUrlsFromWebsiteId', #  (idSite, period, date, idSubtable,
'Referers.getNumberOfDistinctSearchEngines', #  (idSite, period, date,
'Referers.getNumberOfDistinctKeywords', #  (idSite, period, date, segment =
'Referers.getNumberOfDistinctCampaigns', #  (idSite, period, date, segment
'Referers.getNumberOfDistinctWebsites', #  (idSite, period, date, segment =
'Referers.getNumberOfDistinctWebsitesUrls', #  (idSite, period, date,
'SEO.getRank', #  (url) [ Example in [228]XML, [229]Json, [230]Tsv (Excel)
'SitesManager.getJavascriptTag', #  (idSite, piwikUrl = '') [ Example in
'SitesManager.getSitesFromGroup', #  (group) [ No example available ]
'SitesManager.getSitesGroups', #  () [ Example in [235]XML, [236]Json,
'SitesManager.getSiteFromId', #  (idSite) [ Example in [238]XML, [239]Json,
'SitesManager.getSiteUrlsFromId', #  (idSite) [ Example in [241]XML,
'SitesManager.getAllSitesId', #  () [ Example in [244]XML, [245]Json,
'SitesManager.getSitesIdWithVisits', #  (timestamp = '') [ Example in
'SitesManager.getSitesWithAdminAccess', #  () [ Example in [250]XML,
'SitesManager.getSitesWithViewAccess', #  () [ Example in [253]XML,
'SitesManager.getSitesWithAtLeastViewAccess', #  (limit = '') [ Example in
'SitesManager.getSitesIdWithAdminAccess', #  () [ Example in [259]XML,
'SitesManager.getSitesIdWithViewAccess', #  () [ Example in [262]XML,
'SitesManager.getSitesIdWithAtLeastViewAccess', #  () [ Example in
'SitesManager.getSitesIdFromSiteUrl', #  (url) [ Example in [268]XML,
'SitesManager.addSite', #  (siteName, urls, ecommerce = '', excludedIps =
'SitesManager.deleteSite', #  (idSite) [ No example available ]
'SitesManager.addSiteAliasUrls', #  (idSite, urls) [ No example available ]
'SitesManager.getIpsForRange', #  (ipRange) [ No example available ]
'SitesManager.setGlobalExcludedIps', #  (excludedIps) [ No example
'SitesManager.getExcludedQueryParametersGlobal', #  () [ Example in
'SitesManager.setGlobalExcludedQueryParameters', # 
'SitesManager.getExcludedIpsGlobal', #  () [ Example in [274]XML,
'SitesManager.getDefaultCurrency', #  () [ Example in [277]XML, [278]Json,
'SitesManager.setDefaultCurrency', #  (defaultCurrency) [ No example
'SitesManager.getDefaultTimezone', #  () [ Example in [280]XML, [281]Json,
'SitesManager.setDefaultTimezone', #  (defaultTimezone) [ No example
'SitesManager.updateSite', #  (idSite, siteName, urls = '', ecommerce = '',
'SitesManager.getCurrencyList', #  () [ Example in [283]XML, [284]Json,
'SitesManager.getCurrencySymbols', #  () [ Example in [286]XML, [287]Json,
'SitesManager.getTimezonesList', #  () [ Example in [289]XML, [290]Json,
'SitesManager.getUniqueSiteTimezones', #  () [ Example in [292]XML,
'SitesManager.getPatternMatchSites', #  (pattern) [ No example available ]
'UserCountry.getCountry', #  (idSite, period, date, segment = '') [ Example
'UserCountry.getContinent', #  (idSite, period, date, segment = '') [
'UserCountry.getNumberOfDistinctCountries', #  (idSite, period, date,
'UserSettings.getResolution', #  (idSite, period, date, segment = '') [
'UserSettings.getConfiguration', #  (idSite, period, date, segment = '') [
'UserSettings.getOS', #  (idSite, period, date, segment = '') [ Example in
'UserSettings.getBrowser', #  (idSite, period, date, segment = '') [
'UserSettings.getBrowserType', #  (idSite, period, date, segment = '') [
'UserSettings.getWideScreen', #  (idSite, period, date, segment = '') [
'UserSettings.getPlugin', #  (idSite, period, date, segment = '') [ Example
'UsersManager.setUserPreference', #  (userLogin, preferenceName,
'UsersManager.getUserPreference', #  (userLogin, preferenceName) [ No
'UsersManager.getUsers', #  (userLogins = '') [ Example in [336]XML,
'UsersManager.getUsersLogin', #  () [ Example in [339]XML, [340]Json,
'UsersManager.getUsersSitesFromAccess', #  (access) [ Example in [342]XML,
'UsersManager.getUsersAccessFromSite', #  (idSite) [ Example in [345]XML,
'UsersManager.getUsersWithSiteAccess', #  (idSite, access) [ Example in
'UsersManager.getSitesAccessFromUser', #  (userLogin) [ Example in
'UsersManager.getUser', #  (userLogin) [ Example in [354]XML, [355]Json,
'UsersManager.getUserByEmail', #  (userEmail) [ No example available ]
'UsersManager.addUser', #  (userLogin, password, email, alias = '') [ No
'UsersManager.updateUser', #  (userLogin, password = '', email = '', alias
'UsersManager.deleteUser', #  (userLogin) [ No example available ]
'UsersManager.userExists', #  (userLogin) [ Example in [357]XML, [358]Json,
'UsersManager.userEmailExists', #  (userEmail) [ No example available ]
'UsersManager.setUserAccess', #  (userLogin, access, idSites) [ No example
'UsersManager.getTokenAuth', #  (userLogin, md5Password) [ No example
'VisitFrequency.get', #  (idSite, period, date, segment = '', columns = '')
'VisitTime.getVisitInformationPerLocalTime', #  (idSite, period, date,
'VisitTime.getVisitInformationPerServerTime', #  (idSite, period, date,
'VisitorInterest.getNumberOfVisitsPerVisitDuration', #  (idSite, period,
'VisitorInterest.getNumberOfVisitsPerPage', #  (idSite, period, date,
'VisitsSummary.get', #  (idSite, period, date, segment = '', columns = '')
'VisitsSummary.getVisits', #  (idSite, period, date, segment = '') [
'VisitsSummary.getUniqueVisitors', #  (idSite, period, date, segment = '')
'VisitsSummary.getActions', #  (idSite, period, date, segment = '') [
'VisitsSummary.getMaxActions', #  (idSite, period, date, segment = '') [
'VisitsSummary.getBounceCount', #  (idSite, period, date, segment = '') [
'VisitsSummary.getVisitsConverted', #  (idSite, period, date, segment = '')
'VisitsSummary.getSumVisitsLength', #  (idSite, period, date, segment = '')
'VisitsSummary.getSumVisitsLengthPretty',
  )

  def __init__(self, server=settings.PIWIK_SERVER, siteid=settings.PIWIK_SITEID, token_auth=settings.PIWIK_TOKEN):
    assert(server)
    self.server = server
    assert(siteid)
    self.siteid = siteid
    assert(token_auth)
    self.token_auth = token_auth

  def call(self, method, format="json", period="month", date="today", segment=None):
    if method in self.available_methods:
      params = {
        'module': 'API',
        'idSite': self.siteid,
        'token_auth': self.token_auth,

        'method': method,
        'format': format,
        'period': period,
        'date': date,
      }

      if segment is not None:
        params['segment'] = segment

      h = httplib2.Http()
      resp, content = h.request("%s?%s"%(self.server, urllib.urlencode(params)), "GET")

      if resp.has_key('status') and resp['status'] == "200":
        return content
      else:
        raise "wurst"
   

  def getPageVisits(self, page):
    result = self.call('VisitsSummary.getVisits', segment="pageUrl==%s"%(page))
    views = simplejson.loads(result)['value']
    return views

  def getPageActions(self, page):
    result = self.call('VisitsSummary.getActions', segment="pageUrl==%s"%(page))
    try:
        views = simplejson.loads(result)['value']
    except KeyError, e:
        print(str(e))
        print(result)
    return views





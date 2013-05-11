# RobotFileGenerator.py
# (C)2013
# Scott Ernst

from pyaid.dict.DictUtils import DictUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON

from StaticFlow.process.SiteProcessUtils import SiteProcessUtils

#___________________________________________________________________________________________________ RobotFileGenerator
class RobotFileGenerator(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, processor):
        """Creates a new instance of RobotFileGenerator."""
        self._processor = processor
        try:
            self._data = JSON.fromFile(self.definitionPath)
        except Exception, err:
            self._data = [
                {'USER_AGENT':'*'}
            ]

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: definitionPath
    @property
    def definitionPath(self):
        return FileUtils.createPath(self._processor.sourceWebRootPath, '__robots__.def', isFile=True)

#___________________________________________________________________________________________________ GS: targetPath
    @property
    def targetPath(self):
        return FileUtils.createPath(self._processor.targetWebRootPath, 'robots.txt', isFile=True)

#___________________________________________________________________________________________________ GS: targetUrl
    @property
    def targetUrl(self):
        domain = self._processor.siteData.get('DOMAIN', None)
        if not domain:
            return u''
        return SiteProcessUtils.getUrlFromPath(self._processor, domain, self.targetPath)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ write
    def write(self):
        """Doc..."""
        FileUtils.putContents(self._convertDataToText(), self.targetPath)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _convertDataToText
    def _convertDataToText(self):
        """Doc..."""
        out = []
        for agent in self._data:
            agent = DictUtils.lowerDictKeys(agent)
            out.append(u'user-agent: ' + agent.get('user_agent', u'*'))
            out.append(u'sitemap: ' + self._processor.sitemap.sitemapTargetUrl)
        return u'\n'.join(out)

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__


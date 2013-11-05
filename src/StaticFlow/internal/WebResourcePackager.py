# WebResourcePackager.py
# (C)2013
# Scott Ernst

import sys
import getopt

from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils

from StaticFlow.StaticFlowEnvironment import StaticFlowEnvironment
from StaticFlow.process.SiteProcessUtils import SiteProcessUtils

#___________________________________________________________________________________________________ WebResourcePackager
class WebResourcePackager(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of WebResourcePackager."""
        pass

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        """Doc..."""
        self._createLoaderJs()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createLoaderJs
    def _createLoaderJs(self):
        """Doc..."""
        result = SiteProcessUtils.compileCoffeescriptFile(
            FileUtils.createPath(
                StaticFlowEnvironment.rootResourcePath, '..', 'js', 'loader.coffee', isFile=True),
            FileUtils.createPath(
                StaticFlowEnvironment.rootResourcePath, 'web', 'js', isDir=True) )
        if result['code']:
            print 'ERROR: Failed to compile loader.coffee'
            print result
            return False

        print 'COMPILED: loader.js'
        return True

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

####################################################################################################
####################################################################################################

#___________________________________________________________________________________________________ usage
def usage():
    print """
    The WebResourcePackager class...
        -h | --help         - Shows this usage information.
    """

#___________________________________________________________________________________________________ main
def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'h', ['help'])
    except getopt.GetoptError, err:
        print str(err) + '\n'
        usage()
        sys.exit(2)



    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(0)
        else:
            print '\nUnknown argument: ' + o + '. Unable to continue.\n\n'
            usage()
            sys.exit(2)

    c = WebResourcePackager()
    c.run()

####################################################################################################
####################################################################################################

if __name__ == '__main__':
    main()

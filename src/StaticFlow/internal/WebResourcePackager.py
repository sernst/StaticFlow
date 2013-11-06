# WebResourcePackager.py
# (C)2013
# Scott Ernst

import os
import sys
import getopt

from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils
from pyaid.web.coffeescript.CoffeescriptBuilder import CoffeescriptBuilder

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
        if not self._createEngineJs():
            return False

        if not self._createLoaderJs():
            return False

        if not self._createEngineCss():
            return False

        return True

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createEngineJs
    def _createEngineJs(self):
        cb = CoffeescriptBuilder(
            'sflow.api.SFlowApi-exec',
            FileUtils.createPath(StaticFlowEnvironment.rootResourcePath, '..', 'js', isDir=True),
            buildOnly=True)
        target = cb.construct()[0]

        targetFolder = FileUtils.createPath(
                StaticFlowEnvironment.rootResourcePath, 'web', 'js', isDir=True)

        result = SiteProcessUtils.compileCoffeescriptFile(target.assembledPath, targetFolder)
        if result['code']:
            print 'ERROR: Failed compilation of the Static Flow engine'
            print result
            return False

        sourcePath = FileUtils.createPath(targetFolder, target.name + '.js', isFile=True)
        destPath   = FileUtils.createPath(targetFolder, 'engine.js', isFile=True)
        SystemUtils.move(sourcePath, destPath)
        return True

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

#___________________________________________________________________________________________________ _createEngineCss
    def _createEngineCss(self):
        resourcePath = StaticFlowEnvironment.rootResourcePath
        sourceFolder = FileUtils.createPath(resourcePath, '..', 'css', isDir=True)
        targetFolder = FileUtils.createPath(resourcePath, 'web', 'css', isDir=True)

        tempPath = FileUtils.createPath(targetFolder, 'engine.temp.css', isFile=True)
        SystemUtils.remove(tempPath)
        destF = open(tempPath, 'a')

        for item in FileUtils.getFilesOnPath(sourceFolder):
            try:
                f = open(item, 'r')
                destF.write('\n' + f.read())
                f.close()
            except Exception , err:
                print 'ERROR: Failed to read CSS file:', item

        destF.close()
        targetPath = FileUtils.createPath(targetFolder, 'engine.css', isFile=True)
        cmd = SiteProcessUtils.modifyNodeCommand([
            StaticFlowEnvironment.getNodeCommandAbsPath('minify'),
            '"%s"' % tempPath,
            '"%s"' % targetPath ])
        result = SystemUtils.executeCommand(cmd)
        SystemUtils.remove(tempPath)
        if result['code']:
            print 'ERROR: Failed to build CSS engine file at:', targetPath
            return False

        print 'ASSEMBLED: engine.css'
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

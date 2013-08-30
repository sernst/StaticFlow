# SiteDeploymentThread.py
# (C)2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from StaticFlow.enum.DeploymentTypeEnum import DeploymentTypeEnum
from StaticFlow.deploy.S3SiteDeployer import S3SiteDeployer
from StaticFlow.process.SiteProcessor import SiteProcessor


#___________________________________________________________________________________________________ SiteDeploymentThread
class SiteDeploymentThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        super(SiteDeploymentThread, self).__init__(parent, **kwargs)
        self._path       = ArgsUtils.get('rootPath', None, kwargs)
        self._deployType = ArgsUtils.get('deployType', DeploymentTypeEnum.LOCAL_DEPLOY, kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: rootPath
    @property
    def rootPath(self):
        return self._path

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        """Doc..."""

        #-------------------------------------------------------------------------------------------
        # EDIT SETTINGS
        if self._deployType == DeploymentTypeEnum.TEST_DEPLOY:
            remoteProcess = True
            s3Deploy      = False
            forceHtml     = True
            forceAll      = True
            clean         = False
        elif self._deployType == DeploymentTypeEnum.REMOTE_DEPLOY:
            remoteProcess = True
            s3Deploy      = True
            forceHtml     = True
            forceAll      = True
            clean         = True
        else:
            remoteProcess = False
            s3Deploy      = False
            forceHtml     = True
            forceAll      = True
            clean         = False

        #-------------------------------------------------------------------------------------------
        # PROCESS SITE FILES
        sp = SiteProcessor(isRemoteDeploy=remoteProcess, containerPath=self._path, logger=self.log)
        sp.run()

        #-------------------------------------------------------------------------------------------
        # DEPLOY SITE FILES
        try:
            if remoteProcess and s3Deploy:
                ssd = S3SiteDeployer(
                    localRootPath=sp.targetWebRootPath,
                    sourceWebRootPath=sp.sourceWebRootPath,
                    forceHtml=forceHtml,
                    forceAll=forceAll,
                    logger=self.log
                )
                ssd.deploy()
        except Exception, err:
            sp.cleanup()
            self.log.writeError('Deployment Failed', err)
            return 1

        #---------------------------------------------------------------------------------------------------
        # REMOVE DEPLOYED FILES
        self.log.write('TARGET LOCATION: ' + sp.targetWebRootPath)
        if clean:
            sp.cleanup()
            self.log.write('Cleanup process complete')

        self.log.write('Operation complete!')

        return 0

# SiteDeploymentThread.py
# (C)2013
# Scott Ernst

from pyaid.ArgsUtils import ArgsUtils

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

from StaticFlow.enum.DeploymentTypeEnum import DeploymentTypeEnum
from StaticFlow.deploy.S3SiteDeployer import S3SiteDeployer
from StaticFlow.process.Site import Site


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

        #--- SPECIFY SETTINGS
        #       Assign process and deploy settings according to the type of deployment enumerated
        #       when the thread was created
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

        #--- PROCESS SITE FILES
        #       Compile and process the files to the target location on disk, either in the local
        #       test folder, or in a temporary folder created in preparation for remote deployment
        sp = Site(isRemoteDeploy=remoteProcess, containerPath=self._path, logger=self.log)
        sp.run()

        #--- DEPLOY SITE FILES
        #       For remote deployments, upload all the files created to the S3 bucket where the site
        #       is deployed.
        try:
            if remoteProcess and s3Deploy:
                ssd = S3SiteDeployer(
                    localRootPath=sp.targetWebRootPath,
                    sourceWebRootPath=sp.sourceWebRootPath,
                    forceHtml=forceHtml,
                    forceAll=forceAll,
                    logger=self.log)
                ssd.deploy()
        except Exception, err:
            sp.cleanup()
            sp.writeLogError(u'Deployment Failed', error=err)
            return 1


        #--- REMOVE DEPLOYED FILES
        if clean:
            sp.cleanup()
            sp.writeLogSuccess(u'CLEANUP', u'Cleanup process complete')

        sp.writeLog(u'TARGET LOCATION', sp.targetWebRootPath, headerColor=u'#3399FF')
        self.log.write(u'<span style="font-size:16px;color:#3399FF;">Deployment Complete</span>')

        return 0

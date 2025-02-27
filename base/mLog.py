import logging
import time
import os
from time import sleep
import threading
from base.mAndroid import getPhoneInfo


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Log:
    def __init__(self, deviceName):
        deviceAttr = getPhoneInfo(deviceName)
        phone_name = deviceAttr["brand"] + "_" + deviceAttr["model"] + "_" + "android" + "_" + deviceAttr["release"]

        global logger, resultPath, logPath
        resultPath = PATH("../log")
        logPath = os.path.join(resultPath, (phone_name + "_" + time.strftime('%Y%m%d%H%M%S', time.localtime())))
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        self.checkNo = 0
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # create handler,write log
        fh = logging.FileHandler(os.path.join(logPath, "my.log"),encoding="GBK")
        # Define the output format of formatter handler
        formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def getMyLogger(self):
        return self.logger

    def buildStartLine(self, caseNo):
        startLine = "----  " + caseNo + "   " + "   " + "  ----"
        self.logger.info(startLine)

    def buildEndLine(self, caseNo):
        endLine = "----  " + caseNo + "   " + "END" + "   " + "  ----"
        self.logger.info(endLine)
        self.checkNo = 0

    def writeResult(self, result):
        """write the case result(OK or NG)
        :param result:
        :return:
        """
        reportPath = os.path.join(logPath, "report.txt")
        flogging = open(reportPath, "a")
        try:
            flogging.write(result + "\n")
        finally:
            flogging.close()
        pass

    def resultOK(self, caseNo):
        self.writeResult(caseNo + ": OK")

    def resultNG(self, caseNo, reason):
        self.writeResult(caseNo + ": NG--" + reason)

    def checkPointOK(self, driver, caseName, checkPoint):
        """write the case's checkPoint(OK)
        :param driver:
        :param caseName:
        :param checkPoint:
        :return:
        """
        self.checkNo += 1

        self.logger.info("[CheckPoint_" + str(self.checkNo) + "]: " + checkPoint + ": OK")

        # take shot
        self.screenshotOK(driver, caseName)

    def checkPointNG(self, driver, caseName, checkPoint):
        """write the case's checkPoint(NG)
        :param driver:
        :param caseName:
        :param checkPoint:
        :return:
        """
        self.checkNo += 1

        self.logger.info("[CheckPoint_" + str(self.checkNo) + "]: " + checkPoint + ": NG")

        # take shot
        return self.screenshotNG(driver, caseName)

    def screenshotOK(self, driver, caseName):
        """screen shot
        :param driver:
        :param caseName:
        :return:
        """
        screenshotPath = os.path.join(logPath, caseName)
        screenshotName = "CheckPoint_" + str(self.checkNo) + "_OK.png"

        # wait for animations to complete before taking screenshot
        sleep(1)
        # driver.get_screenshot_as_file(os.path.join(screenshotPath, screenshotName))
        driver.get_screenshot_as_file(os.path.join(screenshotPath + screenshotName))

    def screenshotNG(self, driver, caseName):
        """screen shot
        :param driver:
        :param caseName:
        :return:
        """
        screenshotPath = os.path.join(logPath, caseName)
        screenshotName = "CheckPoint_" + str(self.checkNo) + "_NG.png"

        # wait for animations to complete before taking screenshot
        sleep(1)
        driver.get_screenshot_as_file(os.path.join(screenshotPath + screenshotName))
        return os.path.join(screenshotPath + screenshotName)

    def screenshotERROR(self, driver, caseName):
        """screen shot
        :param driver:
        :param caseName:
        :return:
        """
        screenshotPath = os.path.join(logPath, caseName)
        screenshotName = "ERROR.png"

        # wait for animations to complete before taking screenshot
        sleep(1)
        driver.get_screenshot_as_file(os.path.join(screenshotPath, screenshotName))


class myLog:
    """
    This class is used to get log
    """
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def getLog(devices):
        if myLog.log is None:
            myLog.mutex.acquire()
            myLog.log = Log(devices)
            myLog.mutex.release()
        return myLog.log


if __name__ == "__main__":
    logger = myLog.getLog("LE67A06310143950")
    # logger = logger.getMyLogger()
    logger.buildStartLine("logger is running")
    logger.buildEndLine("22")
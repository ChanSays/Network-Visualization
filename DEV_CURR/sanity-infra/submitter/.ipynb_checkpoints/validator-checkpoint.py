""" validate params to validate the submission """

import os
import sys
import glob
from utils.dbconnect import DBConnect
from utils.logger import Logger

log = Logger(__name__)


class Validator:
    args = None

    def __init__(self, args):
        self.args = args

    def validate(self):
        """ Validate all params """
        try:
            dbcon = DBConnect()
            # submitter
            if self.args["submitter"] is None:
                return False, "Submitter is None"

            # testsuite
            if self.args["testsuite"] is None:
                return False, "Testsuite is None"
            else:
                # check if testsuite name is valid
                testsuite_cmd = "select exists (select * from testsuites where testsuite='{0}');".format(
                    self.args["testsuite"])
                suite_exists = dbcon.fetch(testsuite_cmd)[0][0]
                if suite_exists == 0:
                    return False, "Testsuite: {0} does not exist".format(self.args["testsuite"])

            # asic
            if self.args["asic"] != "":
                # check if asic name is valid
                asic_exists_cmd = " select exists (select * from asics where asic='{0}'); ".format(self.args["asic"])
                asic_exists = dbcon.fetch(asic_exists_cmd)[0][0]
                if asic_exists == 0:
                    return False, "Asic: {0} does not exist".format(self.args["asic"])
                # check if asic is unsupported for testsuite
                asic_testbed_cmd = "select unsupported_asics from testsuites" \
                                   " where testsuite='{0}';".format(self.args["testsuite"])
                asics = dbcon.fetch(asic_testbed_cmd)[0][0]
                if asics is not None:
                    for asic in asics.split(","):
                        if asic == self.args["asic"]:
                            reason = "The asic:{asic} doesn't support the testsuite:{testsuite}"
                            reason = reason.format(asic=self.args["asic"],
                                                   testsuite=self.args["testsuite"])
                            return False, reason

            # build
            if self.args["build"] == "":
                if self.args["download_image"] == "":
                    # download image value can only be validated at Sanity Server.
                    return False, "Values for build, and download_image are all None"
            else:
                if not os.path.exists(self.args["build"]):
                    return False, "Build file/folder does not exist"
                # if build is a dir
                elif os.path.isdir(self.args["build"]):
                    # Case 1: when build set to /auto/ins-bld-tools/.../REL.x.x.x.xxx
                    build_path = "/{0}/build/images/final".format(
                        self.args["build"].strip("/"))
                    path_res = glob.glob("{0}/nxos.*.bin".format(build_path))

                    if len(path_res) > 1:
                        return False, "more than 1 nxos.*.bin file exists in {0}".format(
                            build_path)
                    elif len(path_res) < 1:
                        # Case 2: when build set to /.../build/images/final
                        build_path = "/{0}".format(self.args["build"].strip("/"))
                        path_res = glob.glob("{0}/nxos.*.bin".format(build_path))
                        if len(path_res) < 1:
                            return False, "nxos.*.bin file doesn't exists in {0}".format(
                                build_path)
                        elif len(path_res) > 1:
                            return False, "more than 1 nxos.*.bin file exists in {0}".format(
                                build_path)
                # if build is a file
                else:
                    if not self.args["build"].endswith('.bin'):
                        return False, "build is not a .bin file"

            # check ISSU params
            if self.args["issu_build_srcdir"] != "":
                if not os.path.isdir(self.args["issu_build_srcdir"]):
                    return False, "issu_build_srcdir is not a directory"

            # testbed
            if self.args["testbed"] != "":
                testbed_cmd = "select exists (select * from tb_status where testbed = '{0}');".format(
                    self.args["testbed"])
                exists = dbcon.fetch(testbed_cmd)[0][0]
                if exists == 0:
                    return False, "Testbed '{}' does not exist".format(self.args["testbed"])

            return True, "Params valid"
        except Exception as e:
            log.error("Validator failed:"+repr(e))
            sys.exit("Exception caught in Validator")
        finally:
            dbcon.close_connection()

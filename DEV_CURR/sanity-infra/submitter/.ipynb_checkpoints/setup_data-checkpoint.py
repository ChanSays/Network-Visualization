""" set up the job data in pre schedule phase """

import os
import sys
import glob
import shutil
import stat
from utils.dbconnect import DBConnect
from utils.logger import Logger
from utils import constants

log = Logger(__name__)


class SetupJobData:

    job = None

    def __init__(self, job):
        self.job = job

    def create_job_dir(self):
        """ create /vol/eor-qa/sanity/logs/{submitter}/{job_id} dir """
        dir_path = """/vol/eor-qa/sanity/logs/{0}/{1}/""".format(self.job["submitter"],
                                                                 self.job["submit_id"])
        try:
            if os.path.isdir(dir_path):
                # log.debug("path exists:"+repr(dir_path))
                pass
            else:
                log.debug("creating dir "+repr(dir_path))
                os.makedirs(dir_path)
                os.chmod(dir_path, stat.S_IRWXG | stat.S_IRWXU | stat.S_IRWXO)
        except Exception as e:
            log.error("create_log_dir failed:" + repr(e))
            sys.exit(-1)

    def update_job_details(self, column, value):
        """ for updating the submitted job table values """
        try:
            dbcon = DBConnect()
            update_flags = """update submitted_jobs set {column}='{value}' 
                              where submit_id={submit_id} """
            update_flags = update_flags.format(column=column, value=value, submit_id=self.job["submit_id"])
            dbcon.execute(update_flags)
        except Exception as e:
            log.error("update_job_details failed:" + repr(e))
            sys.exit(-1)
        finally:
            dbcon.close_connection()

    def get_image_path(self):
        """ get the image path """
        try:
            img_path = None
            # check if build path is dir or file
            if self.job["build"] != "":
                if os.path.isdir(self.job["build"]):
                    img_path = self.dual_folder_check(self.job["build"], constants.NXOS_BIN)
                else:
                    # Build is an image file (already validated in validator)
                    img_path = self.job["build"]
            else:
                # check build_srcdir
                if self.job["build_srcdir"] != "":
                    img_path = self.dual_folder_check(self.job["build_srcdir"], constants.NXOS_BIN)
            return img_path
        except Exception as e:
            log.error("setup_data failed in get_image_path:"+repr(e))
            sys.exit(-1)

    def get_issu_image_path(self):
        """ get issu image path """
        try:
            issu_img_path = None
            # check issu build_srcdir
            if self.job["issu_build_srcdir"] != "":
                issu_img_path = self.dual_folder_check(self.job["issu_build_srcdir"], constants.ISSU_BIN)
            return issu_img_path
        except Exception as e:
            log.error("setup_data failed in get_issu_image_path:" + repr(e))
            sys.exit(-1)

    def copy_images(self):
        """ copy nxos bin and issu images to /tftpboot/sanity-image """
        try:
            log.debug("Copying images for job")
            # check download_image
            if self.job["download_image"] != "":
                log.debug("checking for image in tftpboot since download_image is set")
                tftp_path = "{0}/{1}".format(constants.TFTP_SAVE_PATH,
                                             self.job["download_image"].strip("/"))
                if not os.path.exists(tftp_path):
                    log.debug("download_image path does not exist: {0}".format(
                        self.job["download_image"]))
                    sys.exit(1)
                self.update_job_details(constants.FINAL_IMAGE_PATH, tftp_path)
                # self.update_final_image_name(tftp_path)
            else:
                # copy nxos bin to /tftpboot
                log.debug("checking to copy image to tftpboot")
                nxos_bin = self.get_image_path()
                if nxos_bin is None:
                    log.debug("Couldn't derive nxos image path")
                    sys.exit(1)
                # copy nxos bin
                dest_image_name = "{0}-{1}-{2}".format(self.job["submitter"], self.job["submit_id"],
                                                       os.path.basename(nxos_bin))
                dest_path = "{0}/{1}".format(constants.TFTP_SAVE_PATH, dest_image_name)
                shutil.copyfile(nxos_bin, dest_path)
                self.update_job_details(constants.FINAL_IMAGE_PATH, dest_path)

                # copy issu nxos bin to /tftpboot
                issu_bin = self.get_issu_image_path()
                if issu_bin is None:
                    return
                dest_issu_name = "{0}-{1}-{2}".format(self.job["submitter"], self.job["submit_id"],
                                                       os.path.basename(issu_bin))
                dest_issu_path = "{0}/{1}".format(constants.TFTP_SAVE_PATH, dest_issu_name)
                shutil.copyfile(issu_bin, dest_issu_path)
                self.update_job_details(constants.FINAL_ISSU_PATH, dest_issu_path)
        except Exception as e:
            log.error("setup_data failed in copy_images:" + repr(e))
            sys.exit(-1)

    def copy_config_files(self):
        """ copy files such as python-env, testbed yml, logical dict etc """
        new_change = ""
        if self.job["newChange"] == constants.NEW_CHANGE:
            new_change = constants.NEW_CHANGE_PATH
        dir_path = """/vol/eor-qa/sanity/logs/{0}/{1}""".format(self.job["submitter"],
                                                                self.job["submit_id"])
        working_dir = "/vol/eor-qa/sanity"
        python_env_file = "{0}/python-env{1}".format(working_dir, new_change)
        logical_dict = "/vol/eor-qa/sanity/jobs/logical_dict{0}.yml".format(new_change)
        try:
            log.debug("copying python_env and logical_dict to log dir.")
            # copy env file
            shutil.copy(python_env_file, dir_path)
            shutil.copy(logical_dict, dir_path)
            # asic might be wildcard and may be decided by the scheduler
            # testbed will be handled in scheduler invoke_job.
        except Exception as e:
            log.error("setup_data failed in copy_config_files:" + repr(e))
            sys.exit(-1)

    def dual_folder_check(self, path, bin_type):
        """ check for bin_type file in the path """
        try:
            # Case 1: when path set to /auto/ins-bld-tools/.../REL.x.x.x.xxx
            build_path = "/{0}/build/images/final".format(path.strip("/"))
            path_res = glob.glob("{0}/{1}".format(build_path, bin_type))
            if len(path_res) == 1:
                return path_res[0]

            # Case 2: when path set to /.../build/images/final
            build_path = "/{0}".format(path.strip("/"))
            path_res = glob.glob("{0}/{1}".format(build_path, bin_type))
            if len(path_res) == 1:
                return path_res[0]

            return None
        except Exception as e:
            log.error("setup_data failed in dual_folder_check:" + repr(e))
            sys.exit(-1)

    def setup_job_data(self):
        """ setup data: images, env, config files, etc.. """
        self.create_job_dir()
        # check download_image flag
        log.debug("Setting up job data for job "+repr(self.job))
        self.copy_images()
        self.copy_config_files()

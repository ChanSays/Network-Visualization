import paramiko
import logging as log
import sanityapp.utils as utils



class SSHClient():
    def __init__(self, address=utils.SSH_Host, username=utils.SSH_Username, password=utils.SSH_Password):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(address, username=username, password=password,allow_agent=False,look_for_keys=False)

    def __del__(self):
        if self.client is not None:
            self.client.close()

    def get_file_contents(self, file_path=None):
        if file_path is None:
            return "File path not given"

        log.info("Getting contents of file: {0}".format(file_path))
        sftp_client = self.client.open_sftp()
        contents = ""
        try:
            remote_file = sftp_client.open(file_path)
            for line in remote_file:
                contents = contents + line
            remote_file.close()
        except Exception as e:
            log.error(e)
            contents = "File {0} contents not found".format(file_path)
        log.info(contents)
        return contents

    def send_command(self, command):
        if self.client:
            try:
                stdin, stdout, stderr = self.client.exec_command(command)
                while not stdout.channel.exit_status_ready():
                    if stdout.channel.recv_ready():
                        all_data = stdout.channel.recv(1024)
                        prev_data = b"1"
                        while prev_data:
                            prev_data = stdout.channel.recv(1024)
                            all_data += prev_data
                        log.debug(str(all_data, "utf8"))
                return True
            except Exception as err:
                log.error(err)
                return False
        else:
            log.error("Connection not opened.")
            return False

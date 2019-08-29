import paramiko
from utils.logger import Logger
from scp import SCPClient
from utils.constants import TFTP_SAVE_PATH

log = Logger(__name__)


class SSHClient():
    def __init__(self, address, username, password):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(address, username=username, password=password,allow_agent=False,look_for_keys=False)

    def __del__(self):
        if self.client is not None:
            self.client.close()

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

    def scp_img(self, src, dest):
        try:
            scp = SCPClient(self.client.get_transport())
            log.debug(f"SCP: Copying {src} to {dest}")
            scp.put(src, remote_path=dest)
            return True
        except Exception as err:
            log.error(err)
            return False

    def check_path_exists(self, file_path):
        try:
            sftp = self.client.open_sftp()
            log.debug(f"Checking if path: {file_path} exists")
            sftp.stat(file_path)
            sftp.close()
            return True
        except Exception as e:
            log.error(e)
            return False

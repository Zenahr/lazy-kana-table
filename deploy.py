import os
import time
from ftplib import FTP
from ftpsync.targets import FsTarget
from ftpsync.ftp_target import FtpTarget
from ftpsync.synchronizers import UploadSynchronizer
from secrets import Config

current_path = os.path.dirname(os.path.abspath(__file__))
local = FsTarget(os.path.join(current_path, 'build', 'prod'))

# Credentials
FTP_ADDRESS = os.environ['FTP_ADDRESS']
FTP_USER = os.environ[Config.username]
FTP_PASSWORD = os.environ[config.password]
FTP_TMP_UPLOAD_PATH = '/tmp_%s' % time.strftime("%Y%m%d-%H%M%S")

# Create temp path for upload
ftp = FTP(host=FTP_ADDRESS, user=FTP_USER, passwd=FTP_PASSWORD)
ftp.mkd(FTP_TMP_UPLOAD_PATH)

# Sync build to temp path
remote = FtpTarget(FTP_TMP_UPLOAD_PATH, FTP_ADDRESS, username=FTP_USER, password=FTP_PASSWORD)
opts = {"force": False, "delete_unmatched": True, "verbose": 6}
s = UploadSynchronizer(local, remote, opts)
s.run()

# Rename old build
ftp.rename('public', 'public_%s' % time.strftime("%Y%m%d-%H%M%S"))

# Make new build public
ftp.rename(FTP_TMP_UPLOAD_PATH, 'public')
ftp.quit()

from common.cli_request import CliRequest
from common.file_template_git_sync_config import GitSyncConfigTemplate
from common.logger import Logger
import os

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                          M A I N                                         |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
log = Logger(__name__)
cli = CliRequest(log, os.environ['ps_path'])

for _, params in cli.mods['git-sync-config'].items():
  GitSyncConfigTemplate(
    desc        = params['desc'],
    username    = params['username'],
    token       = params['token'],
    platform    = params['platform'],
    domain      = params['domain'],
    config_file = params['config_file'],
    home_dir    = params['home_dir']
  )

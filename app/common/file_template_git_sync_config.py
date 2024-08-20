from io import StringIO
from pyinfra.operations import files

class GitSyncConfigTemplate():
  def __init__(self,
    desc,
    username,
    token,
    platform="github",
    domain="github.com",
    backup_dir:str="/git-sync",
    config_path:str="/.config/git-sync/",
    config_file:str="config.yaml",
    home_dir:str='~',
    ):

    self.desc = desc
    self.username = username
    self.token = token
    self.platform = platform
    self.domain = domain
    self.backup_dir = backup_dir
    self.config_path = config_path
    self.config_file = config_file
    self.home_dir = home_dir

    assert(type(self.home_dir)==str and len(self.home_dir)>0)

    self.template = StringIO("""username: {{ username }}
token: {{ token }}
include_wiki: {{ include_wiki }}
include_repos: []
exclude_repos: []
include_orgs: []
exclude_orgs: []
backup_dir: {{ backup_dir }}
include_forks: false
platform: {{ platform }}
server:
  domain: {{ domain }}
  protocol: https
""")

    files.template(
      name          = self.desc,
      src           = self.template,
      dest          = self.home_dir + self.config_path + self.config_file,
      username      = self.username,
      token         = self.token,
      include_wiki  = True,
      backup_dir    = self.home_dir + self.backup_dir,
      platform      = self.platform,
      domain        = self.domain
    )
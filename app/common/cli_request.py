from glob import glob
from pathlib import Path
import os, re, yaml

CONFIG_ROOT_KEY:str = 'polis'
CONFIG_FILE_SUFFIX:str = 'ps'
CONFIG_VARS_PREFIX:str = 'PS_ENV_'
CONFIG_MODS_REGEX:str = '\${[a-z_]+}'

class CliRequest():
  def __init__(self, logger, path="."):
    self.log = logger
    self.log.fn = self.__class__.__name__ + '.' + self.__init__.__name__
    self.path = path
    self.config = self.__load_config(schema={
      CONFIG_ROOT_KEY: {
        'vars': {},
        'mods': {}
      }
    })
    self.log.info("load config files complete.")
    self.vars = self.__load_os(self.config['vars'])
    self.log.info("load environment vars complete.")
    self.mods = self.__parse_mods(self.config['mods'])
    self.log.info("parse mods complete.")

  def __load_config(self, schema:dict) -> dict:
    """Loads one or more configuration files
      :param schema: A schema of the config file
    """
    self.log.fn = self.__class__.__name__ + '.' + self.__load_config.__name__
    root = schema[CONFIG_ROOT_KEY]
    paths = [Path(p) for p in glob(self.path + '/' + '*.' + CONFIG_FILE_SUFFIX + '.yaml')]
    for file in paths:
      self.log.info("processing config file {}".format(file))
      with open(file) as fp:
        data = yaml.safe_load(fp)
        for conf, obj in root.items():
          if conf in data[CONFIG_ROOT_KEY]:
            for key, val in data[CONFIG_ROOT_KEY][conf].items():
              if not key in root[conf]:
                root[conf][key] = val
              else:
                self.log.error("Duplicate key {} found.".format(key), Exception)
      fp.close()
    return root

  def __load_os(self, vars:dict) -> dict:
    """Loads one or more environment variables
      :param vars: A config['vars'] dict
    """
    self.log.fn = self.__class__.__name__ + '.' + self.__load_os.__name__
    for key, val in vars.items():
      if val[:len(CONFIG_VARS_PREFIX)] == CONFIG_VARS_PREFIX:
        var = val[len(CONFIG_VARS_PREFIX):]
        if var in os.environ:
          vars[key] = os.environ[var]
        else:
          self.log.error("PS_ENV {} is not defined.".format(var))
    return vars

  def __parse_mods(self, mods:dict) -> dict:
    """Parse one or more modules
      :param mods: A config['mods'] dict
    """
    self.log.fn = self.__class__.__name__ + '.' + self.__parse_mods.__name__
    ret = {}
    for mod, instance in mods.items():
      ret[mod] = instance
      for name, params in instance.items():
        change = self.__match_var(params)
        ret[mod][name] = change
    return ret

  def __match_var(self, params) -> dict:
    """Match one or more variables
      :param params: A config['mods']['instance']['params'] dict
    """
    self.log.fn = self.__class__.__name__ + '.' + self.__parse_mods.__name__
    ret = {}
    for key, val in params.items():
      list_expr = re.findall(CONFIG_MODS_REGEX, val);
      for expr in list_expr:
        var = expr[2:-1]
        if var in self.vars:
          val = val.replace(expr, self.vars[var])
        else:
          self.log.error('var {} is not found.'.format(expr))
      ret[key] = val
    return ret

import pytest, os

def test_sample_vars(vars):
  assert not vars is None
  assert vars['home_dir'] == os.environ['HOME']

def test_sample_mods(mods):
  assert not mods is None
  assert 'git-sync-config' in mods
  for name, params in mods['git-sync-config'].items():
    assert type(name) == str
    assert type(params) == dict
    assert params['home_dir'] == os.environ['HOME']

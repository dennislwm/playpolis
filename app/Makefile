.PHONY: default apply apply_verbose consume front git-sync-config github-sync gitlab-sync test test_verbose

default: test

apply:
	pyinfra @local $(OPS)

apply_verbose:
	pyinfra @local $(OPS) --debug

consume:
	cd api && consume .

front:
	python 03.frontmatter.py

git-sync-config:
	pyinfra @local 01.pyinfra.py

github-sync: git-sync-config
	sudo docker run --rm --name=git-sync -v $(HOME)/.config/git-sync/config-github.yaml:/git-sync/config.yaml -v $(HOME)/git-sync:/backups ghcr.io/akashrajpurohit/git-sync:latest

gitlab-sync: git-sync-config
	sudo docker run --rm --name=git-sync -v $(HOME)/.config/git-sync/config-gitlab.yaml:/git-sync/config.yaml -v $(HOME)/git-sync:/backups ghcr.io/akashrajpurohit/git-sync:latest

test:
	PYTHONPATH=. pytest --disable-warnings

test_verbose:
	PYTHONPATH=. pytest -v -s --disable-warnings
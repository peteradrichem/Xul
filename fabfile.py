# coding=utf-8

"""Show local and remote repository tip."""


from __future__ import print_function

# Fabric
from fabric.api import env, task, cd
from fabric.operations import local

# Brik
from brik.runs import cmd_run

# Deze fabfile is voor hg.omroep.nl
from brik.config import apps_dict
env.hosts = apps_dict['hg']
env.remote_repo_path = "ab/Xml"


@task
def tip():
    """: local and remote Xml script repository tip."""
    local("hg tip")
    with cd(env.remote_repo_path):
        cmd_run("hg tip")

@task
def host():
    """: show remote `fab' host(s)."""
    for remote_h in env.hosts:
        print(remote_h)

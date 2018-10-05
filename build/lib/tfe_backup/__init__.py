#!/usr/bin/env python
from lib import workspace
from lib import workspace_variables
import os
from subprocess import Popen, PIPE
import shlex
import sys

def _call(cmd):
    p = Popen(shlex.split(cmd), 
            stdout=PIPE,
            stderr=PIPE)
    out, err = p.communicate()
    if err:
        sys.stderr.write(str(err))
        sys.stderr.write("\n")
        sys.exit(1)

def sanitize_path(path):
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path


def parse_workspace(org, _ws, basedir, new_workspace_name=False, filename=False, skip_keys=None):
    if skip_keys is None:
        skip_keys = []
    
    ws = workspace.TFEWorkSpace(org, _ws)
    if not filename:
        _filename = os.path.join(basedir, "{0}.tf".format(_ws))
    else:
        _filename = os.path.join(basedir, "{0}.tf".format(filename))
    if new_workspace_name:
        _ws = new_workspace_name

    with open(_filename, "w") as workspace_file:
        workspace_file.write(
                ws.rendered(force=True, 
                    organization_name="${var.organization}", 
                        workspace_name=_ws
                )
            )
        for _var in ws.variables(new_workspace_name, skip_keys):
            workspace_file.write(_var)


def add_vars(_vars):
    for var in _vars:
        workspace_variables.TFEWorkSpaceVariables.undefined_variables.add(var)


def dump_vars(basedir):
    with open(os.path.join(basedir, "variables.tf"), "w") as vars_file:
        for twsvar in workspace_variables.TFEWorkSpaceVariables.define_variables():
            vars_file.write(twsvar)


def main(opt):
    basedir = sanitize_path(opt.basedir)
    workspace.TFEWorkSpace.base_url = opt.api
    workspace_variables.TFEWorkSpaceVariables.base_url = opt.api
    workspace_variables.TFEWorkSpaceVariables.base_dir = basedir
    print "Org: ", opt.tfe_organization
    
    for _ws in workspace.TFEWorkSpace.list(opt.tfe_organization):
        if opt.tfe_workspace and _ws != opt.tfe_workspace:
            continue
        
        if not opt.output:
            parse_workspace(opt.tfe_organization, _ws, basedir, 
                new_workspace_name=opt.new_workspace_name, 
                skip_keys=opt.skip_keys)
        else:
            parse_workspace(opt.tfe_organization, _ws, basedir, 
                new_workspace_name=opt.new_workspace_name, 
                filename=opt.output, 
                skip_keys=opt.skip_keys)
            
    if opt.add_vars:
        add_vars(opt.add_vars)

    dump_vars(basedir)

    # perform post processing to validate configurations
    os.chdir(sanitize_path(opt.basedir))
    if opt.fmt:
        _call("terraform fmt")

    if opt.init or opt.validate:
        tfvars_file = os.path.join(basedir, "terraform.tfvars")
        with open(tfvars_file, "w") as tfvars:
            for _var in workspace_variables.TFEWorkSpaceVariables.undefined_variables:
                tfvars.write('{0}="{1}"\n'.format(_var, opt.tfe_organization))

    if opt.init:
        _call("terraform init")
    if opt.validate:
        _call("terraform validate")

    if opt.init or opt.validate:
        tfvars_file = os.path.join(basedir, "terraform.tfvars")
        os.unlink(tfvars_file)


if __name__ == '__main__':
    from optparse import OptionParser, OptionGroup
    parser = OptionParser()
    parser.add_option('--api', default='https://app.terraform.io')
    
    parser.add_option('-o', '--org', dest="tfe_organization")
    parser.add_option('-w', '--workspace', dest="tfe_workspace", default=False)
    parser.add_option('--output')
    parser.add_option('--new-ws', dest="new_workspace_name")
    parser.add_option('--vars', action='append', dest='add_vars')
    parser.add_option('--fmt', action='store_true', default=False)
    parser.add_option('--init', action='store_true', default=False)
    parser.add_option('--validate', action='store_true', default=False)
    parser.add_option('-b', '--basedir')
    parser.add_option('--skip', action='append', dest='skip_keys')
    
    opt, args = parser.parse_args()
    main(opt)
    

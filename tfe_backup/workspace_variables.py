import requests
import os
from jinja2 import Template
from functools import partial
import urllib

class TFEWorkSpaceVariables(object):
    base_url = "https://app.terraform.io"
    output_dir = "/tmp"
    session_headers = {
        "Authorization": "Bearer {0}".format(os.environ.get("ATLAS_TOKEN")),
        "Content-Type": "application/vnd.api+json"
    }
    undefined_variables = set()
    _base_dir = os.path.dirname(__file__)
    basedir = os.path.join(os.environ.get("PWD"), "tfe_setup")

    def __init__(self, org, workspace, base_url=False):
        self._org = org
        self._workspace = workspace
        if base_url:
            self.base_url = base_url
        self.api_url = "{0}/api/v2/vars".format(self.base_url)
        self._variable_response = False
        
        self.session = requests.Session()
        self.session.headers = self.session_headers
        self.query_params = "filter%5Borganization%5D%5Bname%5D={org}&filter%5Bworkspace%5D%5Bname%5D={workspace}"
        with open("{0}/templates/workspace_vars.j2".format(self._base_dir)) as vars_template:
            self.vars_template = Template(vars_template.read())

    def variables(self):
        if self._variable_response:
            return self._variable_response
        else:
            resp = self.session.get(self.api_url, 
                params=self.query_params.format(
                    org=self._org,
                    workspace=self._workspace
                )
            )
            resp.raise_for_status()
            self._variables_response = resp.json().get("data")
            return self._variables_response

    def rendered(self, workspace=None, skip_keys=None):
        rendered_templates = []
        
        if skip_keys is None:
            skip_keys = []

        for _vars in self._variables_response:
            vars_data = _vars.get("attributes")
            if vars_data.get("key") in skip_keys:
                continue
            if not workspace:
                vars_data["workspace"] = self._workspace
            else:
                vars_data["workspace"] = workspace
            if not vars_data.get("value"):
                vars_data["value"] = "${var."+vars_data.get("key").lower()+"}"
                self.undefined_variables.add(vars_data.get("key").lower())
            if vars_data.get("hcl"):
                # {{ workspace.split("-")|join("_")|lower }}_{{ key }}
                vars_value = vars_data["value"]
                key_name = "{0}_{1}".format("_".join(self._workspace.split("-")).lower(),
                                            vars_data.get("key").lower())
                vars_data["value"] = "${file(\"${path.module}/"+key_name+"\")}"
                with open(os.path.join(self.basedir, key_name), "w") as key_file:
                    key_file.write(vars_value)
            rendered_templates.append(self.vars_template.render(vars_data))
        return rendered_templates

    @staticmethod
    def define_variables():
        with open("{0}/templates/undefined_vars.j2".format(TFEWorkSpaceVariables._base_dir)) as vars_template:
            vars_template = Template(vars_template.read())
        for var in TFEWorkSpaceVariables.undefined_variables:
            yield vars_template.render({"key": var})


import requests
import os
from jinja2 import Template
from functools import partial
from tfe_backup.tfe_session import TFESession
from tfe_backup.workspace_variables import TFEWorkSpaceVariables
from tfe_backup.team_access import TFETeamAccess
import urllib

class TFEWorkSpace(TFESession):

    def __init__(self, org, workspace, base_url=False, clone=True):
        super()
        self.clone = clone
        self._base_dir = os.path.dirname(__file__)
        self._org = org
        self._workspace = workspace
        if base_url:
            self.base_url = base_url
        self.api_url = "{0}/api/v2/organizations/{org}/workspaces/{workspace}".format(self.base_url,
            org=self._org,
            workspace=self._workspace
        )
        self._workspace_response = False
        self._rendered = False
        self.workspace_variables = []
        self.workspace()

    @staticmethod
    def list(organization):
        url = "{0}/api/v2/organizations/{1}/workspaces".format(
            TFEWorkSpace.base_url,
            organization
        )
        resp = requests.get(url, headers=TFESession.session_headers)
        workspaces = resp.json().get("data")
        for x in workspaces:
            yield x.get("attributes").get("name")


    def undefined_variables(self):
        tws_vars = TFEWorkSpaceVariables(self._org, self._workspace)
        tws_vars.variables()
        for ws_var in tws_vars.define_variables():
            yield ws_var

    def variables(self, workspace=None, skip_keys=None):
        if skip_keys is None:
            skip_keys = []
        
        tws_vars = TFEWorkSpaceVariables(self._org, self._workspace)
        tws_vars.variables()
        for ws_var in tws_vars.rendered(workspace, skip_keys):
            yield ws_var

    def team_access(self, workspace):
        team_access = TFETeamAccess(self._workspace, self._workspace_id)
        for ta_access in team_access.rendered(workspace):
            yield ta_access

    def workspace(self):
        if self._workspace_response:
            return self._workspace_response
        else:
            resp = self.session.get(self.api_url)
            resp.raise_for_status()
            self._workspace_response = resp.json().get("data").get("attributes")
            self._workspace_id = resp.json().get("data").get("id")
            return self._workspace_response


    def rendered(self, organization_name=None, workspace_name=None, force=False):
        with open("{0}/templates/workspace.j2".format(self._base_dir)) as workspace_template:
            self.ws_template = Template(workspace_template.read())

        if self._rendered and not force:
            return self._rendered
        else:
            working_directory = self._workspace_response.get("working-directory")
            if not working_directory:
                working_directory = []

            vcs_repo_data = dict()
            vcs_repo = self._workspace_response.get("vcs-repo")
            if vcs_repo:
                for k, v in vcs_repo.items():
                    if "-" in k:
                        vcs_repo_data["_".join(k.split("-"))] = v
                    else:
                        vcs_repo_data[k] = v
                ing_submod = vcs_repo_data["ingress_submodules"]
                vcs_repo_data["ingress_submodules"] = str(ing_submod).lower()
                vcs_repo_data["oauth_token_id"] = "${var.oauth_token_id}"

            almost_rendered = partial(self.ws_template.render,
                vcs_repo=vcs_repo_data,
                working_directory=working_directory,
                terraform_version=self._workspace_response.get("terraform-version"), 
            )
            if not self.clone:
                almost_rendered = partial(almost_rendered, 
                    organization=self._org,
                    workspace_name=self._workspace)
            
            if self.clone and organization_name:
                almost_rendered = partial(almost_rendered, 
                    organization=organization_name)
            
            if self.clone and workspace_name:
                almost_rendered = partial(almost_rendered, 
                    workspace_name=workspace_name)
            
            else:
                almost_rendered = partial(almost_rendered, 
                    organization="${var.organzation}",
                    workspace_name="${var.workspace}")
            self._rendered = almost_rendered()
            return self._rendered
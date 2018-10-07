import requests
import os
from jinja2 import Template
from functools import partial
from tfe_backup.tfe_session import TFESession
from tfe_backup.workspace_variables import TFEWorkSpaceVariables
import urllib

class TFETeamAccess(TFESession):

    def __init__(self, workspace, workspace_id, base_url=False, clone=True):
        super()
        self.clone = clone
        self._base_dir = os.path.dirname(__file__)
        self._workspace = workspace
        self._workspace_id = workspace_id
        self.session = requests.Session()
        self.session.headers = self.session_headers
        if base_url:
            self.base_url = base_url
        self.api_url = "{0}/api/v2/team-workspaces?filter%5Bworkspace%5D%5Bid%5D={1}".format(
            self.base_url,
            self._workspace_id
        )
        with open("{0}/templates/team_access.j2".format(self._base_dir)) as team_access_template:
            self.ta_template = Template(team_access_template.read())

    def rendered(self, workspace):
        resp = self.session.get(self.api_url)
        ta_data = resp.json().get("data")
        for ta in ta_data:
            access = ta.get("attributes").get("access")
            team_id = ta.get("relationships").get("team").get("data").get("id")
            yield self.ta_template.render(
                access=access,
                team_id=team_id,
                workspace=workspace
            )

    
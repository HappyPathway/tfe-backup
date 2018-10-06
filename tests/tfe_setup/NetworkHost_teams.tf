resource "tfe_team_access" "NetworkHost_team_pmgpaueuess9y8ab" {
  access       = "write"
  team_id      = "team-pmGpaUEUESS9Y8AB"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
}

resource "tfe_team_access" "NetworkHost_team_lpsr8hfhbxmd1xkc" {
  access       = "read"
  team_id      = "team-LpSr8hfhBXMd1XkC"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
}

resource "tfe_workspace" "NetworkHost" {
  name         = "NetworkHost"
  organization = "${var.organization}"

  terraform_version = "0.11.8"

  vcs_repo = {
    identifier         = "HappyPathway/aws-network-hosts"
    branch             = "master"
    oauth_token_id     = "${var.oauth_token_id}"
    ingress_submodules = true
  }
}

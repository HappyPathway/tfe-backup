resource "tfe_variable" "NetworkHost_AWS_ACCESS_KEY_ID" {
  key          = "AWS_ACCESS_KEY_ID"
  value        = "${var.aws_access_key_id}"
  category     = "env"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_AWS_DEFAULT_REGION" {
  key          = "AWS_DEFAULT_REGION"
  value        = "us-east-1"
  category     = "env"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_AWS_SECRET_ACCESS_KEY" {
  key          = "AWS_SECRET_ACCESS_KEY"
  value        = "${var.aws_secret_access_key}"
  category     = "env"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = true
}

resource "tfe_variable" "NetworkHost_CONFIRM_DESTROY" {
  key          = "CONFIRM_DESTROY"
  value        = "1"
  category     = "env"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_env" {
  key          = "env"
  value        = "production"
  category     = "terraform"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_instance_type" {
  key          = "instance_type"
  value        = "t2.micro"
  category     = "terraform"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_jenkins_job" {
  key          = "jenkins_job"
  value        = "SimpleApp"
  category     = "terraform"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_network_ws" {
  key          = "network_ws"
  value        = "Network"
  category     = "terraform"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_organization" {
  key          = "organization"
  value        = "TFEBackupTest"
  category     = "terraform"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_public_instances" {
  key          = "public_instances"
  value        = "1"
  category     = "terraform"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_resource_tags" {
  key          = "resource_tags"
  value        = "${file("${path.module}/NetworkHost_resource_tags")}"
  category     = "terraform"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = true
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_vault_addr" {
  key          = "vault_addr"
  value        = "${var.vault_addr}"
  category     = "terraform"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_VAULT_ADDR" {
  key          = "VAULT_ADDR"
  value        = "${var.vault_addr}"
  category     = "env"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_vault_policies" {
  key          = "vault_policies"
  value        = "${file("${path.module}/NetworkHost_vault_policies")}"
  category     = "terraform"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = true
  sensitive    = false
}

resource "tfe_variable" "NetworkHost_VAULT_TOKEN" {
  key          = "VAULT_TOKEN"
  value        = "${var.vault_token}"
  category     = "env"
  workspace_id = "${tfe_workspace.NetworkHost.id}"
  hcl          = false
  sensitive    = true
}

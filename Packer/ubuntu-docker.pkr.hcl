packer {
  required_plugins {
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = "~> 1.0"
    }
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = "~> 1.0"
    }
  }
}

variable "project_id" {
  type    = string
  default = "project-ea36f309-c412-40a0-8d1"
}

variable "zone" {
  type    = string
  default = "europe-west1-b"
}

source "googlecompute" "minecloud" {
  project_id   = var.project_id
  source_image_family = "ubuntu-2204-lts"
  zone         = var.zone
  disk_size    = 20
  ssh_username = "packer"
  image_name   = "minecloud-base-v1-{{timestamp}}"
}

build {
  sources = ["source.googlecompute.minecloud"]

  provisioner "ansible" {
    playbook_file = "../ansible/playbook.yml"
    roles_path    = "../ansible/roles"
    user          = "packer"
    use_proxy     = false
  }
}

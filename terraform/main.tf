provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

data "google_compute_image" "minecloud" {
  name    = var.image_name
  project = var.project_id
}

resource "google_compute_instance" "minecraft_server" {
  name         = "minecloud-server"
  machine_type = "e2-medium"
  zone         = var.zone
  tags         = ["minecraft-server"]

  metadata = {
    ssh-keys = "devops:${file("~/.ssh/minecloud_key.pub")}"
  }

  boot_disk {
    initialize_params {
      image = data.google_compute_image.minecloud.self_link
      size  = 20
      type  = "pd-ssd"
    }
  }

  network_interface {
    network = "default"
    access_config {
      # Laisse vide pour IP publique
    }
  }
}

resource "google_compute_firewall" "allow_minecraft" {
  name    = "allow-minecraft-access"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["25565", "5000", "22", "19999"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["minecraft-server"]
}

output "server_ip" {
  value = google_compute_instance.minecraft_server.network_interface.0.access_config.0.nat_ip
}

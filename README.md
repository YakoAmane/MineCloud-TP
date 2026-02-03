⛏️ MineCloud-TP

MineCloud est une solution d'automatisation complète pour le déploiement de serveurs Minecraft sur Google Cloud Platform (GCP). Le projet implémente les piliers du DevOps : Infrastructure as Code (IaC), Immutable Infrastructure et Configuration Management.
# Stack Technique

    Provisioning : Terraform (Gestion des ressources GCP : VM, VPC, Firewall).

    Image Building : Packer (Création d'une Golden Image Ubuntu pré-configurée avec Docker).

    Configuration : Ansible (Hardening du système et déploiement des conteneurs).

    Monitoring : Interface web via Flask pour le statut du serveur en temps réel.

    Orchestration : Script Bash unifié pour le pilotage du workflow.

# Architecture du Projet

Le déploiement suit un cycle de vie strict pour garantir la reproductibilité :

    Build : Packer génère une image système optimisée.

    Deploy : Terraform déploie l'instance à partir de cette image.

    Configure : Ansible finalise le setup applicatif (Docker Minecraft).

    Expose : Flask fournit une API/Interface de monitoring.

# Quick Start

1. Prérequis

    Un compte GCP avec un projet actif.

    Outils installés : gcloud, terraform, ansible, packer.

    Authentification configurée : gcloud auth application-default login.

2. Déploiement en une commande

Le script deploy.sh automatise l'enchaînement des outils.
Bash

# Rendre le script exécutable
chmod +x deploy.sh

# Lancer l'infrastructure complète
./deploy.sh

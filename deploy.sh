#!/bin/bash

# Arrêter le script si une commande échoue
set -e

echo "🚀 Démarrage du déploiement One-Click MineCloud..."

# --- ÉTAPE 1 : INFRASTRUCTURE (Terraform) ---
echo "--------------------------------------------------"
echo "🏗️  Mise à jour de l'infrastructure avec Terraform..."
echo "--------------------------------------------------"

cd terraform
terraform init
terraform apply -auto-approve

# Récupération automatique de l'IP du serveur depuis Terraform
SERVER_IP=$(terraform output -raw server_ip)

echo "✅ Infrastructure déployée. IP du serveur : $SERVER_IP"

# --- ÉTAPE 2 : CONFIGURATION (Ansible) ---
echo "--------------------------------------------------"
echo "🎮 Déploiement de l'application avec Ansible..."
echo "--------------------------------------------------"

cd ..

# Création automatique du fichier d'inventaire avec la bonne IP
echo "[minecloud]" > inventory.ini
echo "$SERVER_IP" >> inventory.ini

# Attente de sécurité pour être sûr que le SSH est prêt sur le serveur
echo "⏳ Attente de 10 secondes pour l'initialisation SSH..."
sleep 60

# Lancement du playbook
# On désactive la vérification de la clé hôte (Host Key Checking) pour éviter le prompt "yes/no"
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook -i inventory.ini ansible/deploy.yml

echo "--------------------------------------------------"
echo "🎉 DÉPLOIEMENT TERMINÉ AVEC SUCCÈS !"
echo "--------------------------------------------------"
echo "🌍 Minecraft : $SERVER_IP:25565"
echo "📊 Monitoring : http://$SERVER_IP:5000"

#!/bin/bash
set -e
echo "One-Click MineCloud"
echo "E1 Terraform"
cd terraform
terraform init
terraform apply -auto-approve
SERVER_IP=$(terraform output -raw server_ip)
echo "IP du serv : $SERVER_IP"
echo "E2 Ansible"
cd ..
echo "[minecloud]" > inventory.ini
echo "$SERVER_IP" >> inventory.ini
sleep 60
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook -i inventory.ini ansible/deploy.yml
echo "IP srv : $SERVER_IP:25565"
echo "Page de monitoring : http://$SERVER_IP:5000"

#!/usr/bin/env bash
# Docker Engine e Compose para Linux Mint 22.x (base Ubuntu Noble).
# Referência: https://docs.docker.com/engine/install/ubuntu/
set -euo pipefail

source /etc/os-release
if [[ "${UBUNTU_CODENAME:-}" != "noble" ]]; then
  echo 'Este roteiro foi preparado para Linux Mint com base Ubuntu Noble.'
  exit 1
fi

echo 'Instalando Docker pelo repositório oficial. O sudo solicitará sua senha local.'
sudo -v
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
docker_arch=$(dpkg --print-architecture)
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: noble
Components: stable
Architectures: ${docker_arch}
Signed-By: /etc/apt/keyrings/docker.asc
EOF
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo docker run --rm hello-world
sudo docker compose version
echo 'Docker instalado e verificado. Você já pode iniciar o n8n com sudo docker compose up -d.'

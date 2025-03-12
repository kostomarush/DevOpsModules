# На Master и Worker
1. Отключил файл подкачки swap:
```bash
sudo swapoff -a
sed -i '/swap/d' /etc/fstab
```
2. Настроил модули ядра и sysctl для работы с iptables:
```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
#позволяет iptables управлять трафиком, проходящим через мостовые интерфейсы (бриджи)
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
```

```bash
sysctl net.ipv4.ip_forward
```
3. Установка *containerd*:
```bash
sudo apt update && sudo apt install -y containerd
sudo mkdir -p /etc/containerd #создание каталога для конфигурационного файла containerd
containerd config default | sudo tee /etc/containerd/config.toml > /dev/null #Для создания явного конфига containerd
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml # для стабилности управления контейнерами через systemd а не через cgroupfs
sudo systemctl restart containerd
```

4. Установка **kubeadm**, **kubelet** и **kubectl**:

Добавлить GPG-ключ и репозиторий Kubernetes:
```bash
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
```
Установка **kubeadm**, **kubelet** и **kubectl**:
``` bash
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl #так как должны 
оставаться на одной версии для стабильности
sudo systemctl enable --now kubelet
```

## Master:
`sudo kubeadm init --pod-network-cidr=192.168.0.0/16` - задаёт CIDR-диапазон для сетевого плагина (Calico).

Настройка kubectl:
```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config /
#Для подключения kubectl к кластеру
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Установка сетевого плагина Calico:
```bash
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/calico.yaml
```
Проверка подов в control plane:
`kubectl get pods -n kube-system`

Узнать токен для подлкючения worker: `kubeadm token create --print-join-command`

## Worker:

Подключить worker к кластеру:
```bash
kubeadm join <master-ip>:6443 --token <your-token> --discovery-token-ca-cert-hash sha256:<hash>

```

Проверка на master `kubectl get nodes`
`kubectl get pods -n kube-system`

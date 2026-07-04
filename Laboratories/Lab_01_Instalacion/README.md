# Lab 01 — Instalación del entorno

## Objetivo

Configurar el entorno necesario para ejecutar el simulador F1Tenth utilizando ROS 2 Humble en Ubuntu 22.04.

## Requisitos

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- Git
- colcon
- RViz
- VS Code

## 1. Actualizar Ubuntu

```bash
sudo apt update
sudo apt upgrade -y
```

## 2. Instalar Git

```bash
sudo apt install git -y
```

Verificar:

```bash
git --version
```

## 3. Verificar ROS 2 Humble

```bash
ros2 --version
```

También se puede comprobar con:

```bash
printenv ROS_DISTRO
```

El resultado esperado es:

```text
humble
```

## 4. Crear el workspace

```bash
mkdir -p ~/f1tenth_ws/src
cd ~/f1tenth_ws
```

## 5. Compilar el workspace

```bash
colcon build
```

## 6. Cargar el entorno

```bash
source /opt/ros/humble/setup.bash
source ~/f1tenth_ws/install/setup.bash
```

## Resultado esperado

El workspace debe compilar sin errores críticos y ROS 2 debe reconocer los paquetes instalados.
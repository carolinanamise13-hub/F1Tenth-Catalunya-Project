# Lab 02 — Simulador F1Tenth y circuito Catalunya

## Objetivo

Configurar y ejecutar el simulador F1Tenth utilizando el circuito Catalunya.

## Estructura principal

El paquete del simulador se encuentra en:

```text
src/f1tenth_gym_ros/
```

Los mapas se encuentran en:

```text
src/f1tenth_gym_ros/maps/
```

## Archivos del circuito Catalunya

```text
Catalunya_map.png
Catalunya_map.yaml
```

Ruta completa:

```text
src/f1tenth_gym_ros/maps/Catalunya_map.png
src/f1tenth_gym_ros/maps/Catalunya_map.yaml
```

## 1. Verificar los mapas

```bash
ls ~/f1tenth_ws/src/f1tenth_gym_ros/maps
```

Se debe observar:

```text
Catalunya_map.png
Catalunya_map.yaml
```

## 2. Configurar el simulador

El archivo principal de configuración es:

```text
src/f1tenth_gym_ros/config/sim.yaml
```

Este archivo debe apuntar al mapa Catalunya.

## 3. Compilar

```bash
cd ~/f1tenth_ws
colcon build
```

## 4. Cargar ROS 2

```bash
source /opt/ros/humble/setup.bash
source ~/f1tenth_ws/install/setup.bash
```

## 5. Ejecutar el simulador

```bash
ros2 launch f1tenth_gym_ros gym_bridge_launch.py
```

## Resultado esperado

RViz debe abrirse mostrando:

- circuito Catalunya
- vehículo F1Tenth
- información LiDAR
- posición del vehículo
- mapa de ocupación

## Capturas

Las capturas del simulador se almacenan en:

```text
img/simulador/
```
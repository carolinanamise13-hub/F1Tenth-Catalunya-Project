# Lab 03 — Controlador Follow the Gap

## Objetivo

Implementar un controlador autónomo basado en LiDAR utilizando el algoritmo Follow the Gap.

## Paquete ROS 2

El paquete desarrollado se encuentra en:

```text
src/gap_follow/
```

El controlador principal está en:

```text
src/gap_follow/gap_follow/gap_node.py
```

El contador de vueltas está en:

```text
src/gap_follow/gap_follow/lap_counter.py
```

## Funcionamiento general

El algoritmo Follow the Gap utiliza los datos del LiDAR para encontrar una región libre por donde conducir.

Flujo general:

1. Recibir datos del LiDAR.
2. Eliminar valores inválidos.
3. Limitar el rango máximo.
4. Detectar el obstáculo más cercano.
5. Crear una burbuja de seguridad.
6. Buscar el espacio libre más grande.
7. Seleccionar el mejor punto objetivo.
8. Calcular el ángulo de dirección.
9. Ajustar dinámicamente la velocidad.
10. Publicar el comando de conducción.

## Topics utilizados

### Entrada LiDAR

```text
/scan
```

Tipo:

```text
sensor_msgs/msg/LaserScan
```

### Salida de conducción

```text
/drive
```

Tipo:

```text
ackermann_msgs/msg/AckermannDriveStamped
```

## Parámetros principales

Ejemplo:

```python
self.max_range = 8.0
self.bubble_radius = 18
self.safety_distance = 1.2
self.max_steering_angle = 0.42
```

### max_range

Distancia máxima LiDAR utilizada por el controlador.

### bubble_radius

Tamaño de la zona de seguridad creada alrededor del obstáculo más cercano.

### safety_distance

Distancia mínima deseada respecto a los obstáculos.

### max_steering_angle

Ángulo máximo permitido para la dirección.

## Compilar

```bash
cd ~/f1tenth_ws
colcon build --packages-select gap_follow
```

## Cargar el entorno

```bash
source ~/f1tenth_ws/install/setup.bash
```

## Ejecutar el controlador

```bash
ros2 run gap_follow gap_node
```

## Resultado esperado

El vehículo debe:

- seguir la pista Catalunya
- reaccionar a curvas
- evitar paredes
- reducir velocidad en curvas cerradas
- aumentar velocidad en rectas
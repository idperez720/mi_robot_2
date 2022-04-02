# mi_robot_2
En este documento se indica como usar correctamente el código del paquete de ROS para operar un robot diferencial remotamente. Para esto es necesario dos maquinas para ejecutar los códigos. De esta manera, la primera será desde donde se va a enviar las acciones de control y la segunda la que va a ejecutar las acciones en el robot. Para el caso implementado, la primera correspondería al PC y la segunda a la Raspberry del robot.

Para lograr el correr el paquete correctamente es importante configurar ambas maquinar correctamente, esto se puede lograr de la siguiente manera.

## Configuración del entorno.
### Paso 1: Ejecutar `sudo su` en las terminales de ambas maquinas.
Este paso es importante, pues varios de los códigos de los nodos del paquete necesitan permisos root para ser ejecutados.
### Paso 2: Entrar al directorio del espacio de trabajo.
En nuestro caso el directorio era `catkin_ws`
### Paso 3: Ejecutar el comando `roscore`en la maquina que va a enviar las acciones de control.
En nuestro caso era el pc, por lo que en una terminal se ejecutó el comando y se dejó corriendo.
### Paso 4: Configurar ROS_MASTER_URI y ROS_IP en ambas maquinas.
Este paso es de los más importantes, pues es de vital importancia para el correcto funcionamiento del paquete. Para esto en ambas terminales se debe ejecutar los siguientes comandos:

    export ROS_MASTER_URI=http://[ipRoscore]:11311
    export ROS_IP=[ipRoscore]
   ipRoscore corresponde a la ip de la maquina en la que se está corriendo el roscore (sin "[" y "]"). Ejemplo:
   
	export ROS_MASTER_URI=http://172.0.0.1:11311
    export ROS_IP=172.0.0.1
### Paso 5: Ejecutar `source devel/setup.bash` en el espacio de trabajo.
En este paso se debe ejecutar el comando en la carpeta del espacio de trabajo. En nuestro caso está carpeta correspondía a `catkin_ws`
#
Una vez terminado estos paso, el entorno ya quedaría configurado. No sobra mencionar que ambas maquinas deben estar en la misma red.

Por ultimo, para ejecutar los nodos se debe tener en cuenta lo siguiente:
1. El nodo `robot_listener` es el encargado de ejecutar las acciones de control. En otras palabras es el encargado de accionar los motores según lo indicado por la maquina principal.
2. El nodo `robot_teleop` es el encargado de la operación remota del robot. Al ejecutarlo se le preguntará sobre las velocidades deseadas, y si desea guardar o no el recorrido ejecutado por el robot. Y finalmente en la fase de operación podrá controlar el movimiento del robot usando las teclas WASD las cuales corresponde: W mover hacia adelante, S mover hacia atrás, A girar hacia la izquierda, y D girar a la derecha.

Si desea más información sobre el desarrollo y funcionamiento de los nodos implementados, puede leer el archivo pdf que se encuentra en la carpeta `results` de este mismo paquete.

## Ejecución de los nodos. 
Es importante dejar claro, que para la correcta ejecución de los nodos primero se debe correr el nodo que va a operar las funciones, ya sea el nodo `robot_teleop` o el nodo `robot_player`. Una recomendación para este ultimo es que antes de confirmar el archivo del recorrido se corran lo nodos auxiliares que se quieran utilizar, ya sea `robot_interface`o `robot_listener`.`

# Guida

1. inserire alla fine del file ~/.bashrc la stringa source ~/catkin_ws/devel/setup.bash
```bash
nano ~/.bashrc
source ~/catkin_ws/devel/setup.bash
```

2. copiare e incolare la cartella py_robot (inerente al packege Ros) nella cartella ~/catkin_ws/src/


3. aprire un terminale e digitare:
```bash
cd ~/catkin_ws/
catkin_make
```
4. ripetere il punto 3 per ogni volta che si aggiungono file al packege

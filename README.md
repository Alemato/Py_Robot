# Py Robot Project
## Descrizione 
Il Problema "Z" che il rover dovrà risolvere è il seguente:

Cercare e riconoscere un QR code all'interno di un ambiente circoscritto, nel quale il rover naviga.
Una volta travto tale QR Code il Rover emettera un suono tramite un Buzzer. 

# Specifice Hardware

## Lista dei componenti da aggiungere al Rover 
### Sono i componenti che vorremmo implementare nel progetto.
###### Componenti già in possesso (durante il progetto)
* 1x OpenMV camera 
* 1x Servomotore (di proprietà di Alessandro Mattei)
* 1x Buzzer, Cicalino Attivo (di proprietà di Alessandro Mattei)

###### Componenti compranti durante il progetto
* 1x Microswitch con levetta (il linck a seguire sono 10 pz e li useremo tutti) [(acquistato dal gruppo)](https://www.amazon.it/ROSENICE-Pezzi-Interruttore-Levetta-Micro/dp/B01JRORHGE)
* 1x MakerHawk Lidar Laser Range Modulo Modulo a Singolo Punto Micro Range Pixhawk Compatibile con Cavo  [(acquistato dall'Università)](https://www.amazon.it/MakerHawk-Modulo-Singolo-Pixhawk-Compatibile/dp/B0778B15G7/ref=sr_1_1?ie=UTF8&qid=1517130708&sr=8-1&keywords=lidar)
* 2x Dual Motor Driver 1A TB6612FNG Microcontroller [(acquistato dall'Università)](https://www.amazon.it/Cylewet-TB6612FNG-Arduino-Replace-confezione/dp/B071KSTWK8/ref=sr_1_2?ie=UTF8&qid=1517130339&sr=8-2&keywords=TB6612FNG)
* 1x Multistar LiHV ad alta capacità 5200mAh 3S multi-rotore Lipo pack [(acquistato dall'Università)](https://www.amazon.it/Multistar-LiHV-Capacity-5200mAh-Multi-Rotor/dp/B01BJCZ2G4/ref=sr_1_1?ie=UTF8&qid=1517130402&sr=8-1&keywords=LiHV+5200mAh)
* 2x Lipo Voltage Checker (2S - 8S) [(acquistato dall'Università)](https://www.amazon.it/WOSKY-Battery-Indicator-helicopter-quadcopter/dp/B072J71G72/ref=sr_1_2?ie=UTF8&qid=1517130448&sr=8-2&keywords=Lipo+Voltage+Checker)
* 1x Turnigy Accucel-6 80W 10A Balancer / Charger LiHV Capace [(acquistato dall'Università)](https://hobbyking.com/it_it/turnigy-accucel-6-80w-10a-balancer-charger-lihv-capable.html)
* 1x Turnigy Temperature Sensor for Battery Charger [(acquistato dall'Università)](https://hobbyking.com/it_it/turnigy-temperature-sensor-for-battery-charger.html)
* 1x Turnigy ignifugo LiPoly Bag Batteria (zip) (200x155x95mm) [(acquistato dall'Università)](https://hobbyking.com/it_it/fire-retardant-lipo-battery-bag-220x155x115mm-with-handle.html)
* 1x Sacco 18x22cm ai polimeri di litio ricarica Confezione [(acquistato dall'Università)](https://hobbyking.com/it_it/lithium-polymer-charge-pack-18x22cm-sack.html)


## Lista dei componenti da acquistare per il nostro progetto 
###### Sono i componenti che vorremmo implementare nel NOSTRO progetto e che dovranno essere acquistati.

# Specifiche Software

### Specifiche richieste del Professore 
* Cambiare OS da Raspbian a [Ubuntu-Mate 16.04.2](https://ubuntu-mate.org/raspberry-pi)
* Implementare [Ros Kinetic](http://wiki.ros.org/kinetic) come Publish-Subscribe al posto MQTT 

### Specifiche Aggiuntuve (in forse)
* Dashboard di controllo e monitoraggio del Rover su un sistema esterno tramite ROS rqt
* Streaming video catturato della Pi camera e riprodotto sulla dashboard tramite ROS rqt
* Modifica degli sketch degli arduini, standardizzazione in nodi ROS (in fase di Test)

## Funzione del Microswitch con levetta
Data la scarsa precisone nel rilevare gli ostacoli sottili, ad esempio un piede della sedia, da parte dei tre sensori ad ultrasuoni, i Microswitch con levetta risolveranno tale problema funzionando come un Bumper Sensor.  

## Funzione del sensore di distanza
Uso del sensore Sharp GP2Y0A21 Distance Sensor mosso da servomotore per scandagliare l'ambiente antistante il rover in cerca della strada più libera. Tale rilevatore verrà attivato nell'istante in cui uno più sensori riconosceranno un ostacolo.

## Lista Cartelle e descrizione contenuto

>
Py_Robot: cartella pricipale che contiene tutto il progetto
>>
Arduini: cartella che contiene tutti gli sketch
>>
PORT: cartella che contiene i programmi python per i seriali
>>
py_robot: packege Ros del progetto
>>
RobotVrep: cartella che contine tutti i programmi per simulare il robot all'interno di vrep

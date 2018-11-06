# Py Robot Project
## Descrizione 
Il Problema "Z" che il rover dovrà risolvere è il seguente:

Cercare e riconoscere un QR code all'interno di un ambiente circoscritto, nel quale il rover naviga in totale sicurezza evitando gli ostacoli tramite i sensori ultrasuoni e la Pi-Camera.
Una volta travto tale QR Code il Rover accendera il led della OpenMV Camera. 

# Specifice Hardware

## Lista dei componenti da aggiungere al Rover 
### Sono i componenti che vorremmo implementare nel progetto.
###### Componenti già in possesso (durante il progetto)
* 1x OpenMV camera 

###### Componenti compranti durante il progetto
* 1x Microswitch con levetta (il linck a seguire sono 10 pz e li useremo tutti) [(acquistato dal gruppo)](https://www.amazon.it/ROSENICE-Pezzi-Interruttore-Levetta-Micro/dp/B01JRORHGE)
* 1x MakerHawk Lidar Laser Range Modulo Modulo a Singolo Punto Micro Range Pixhawk Compatibile con Cavo  [(acquistato dall'Università)](https://www.amazon.it/MakerHawk-Modulo-Singolo-Pixhawk-Compatibile/dp/B0778B15G7/ref=sr_1_1?ie=UTF8&qid=1517130708&sr=8-1&keywords=lidar)
* 1x Multistar LiHV ad alta capacità 5200mAh 3S multi-rotore Lipo pack [(acquistato dall'Università)](https://www.amazon.it/Multistar-LiHV-Capacity-5200mAh-Multi-Rotor/dp/B01BJCZ2G4/ref=sr_1_1?ie=UTF8&qid=1517130402&sr=8-1&keywords=LiHV+5200mAh)
* 1x Set 2 Lipo Voltage Checker (2S - 8S) [(acquistato dall'Università)](https://www.amazon.it/WOSKY-Battery-Indicator-helicopter-quadcopter/dp/B072J71G72/ref=sr_1_2?ie=UTF8&qid=1517130448&sr=8-2&keywords=Lipo+Voltage+Checker)
* 1x Turnigy Accucel-6 80W 10A Balancer / Charger LiHV Capace [(acquistato dall'Università)](https://hobbyking.com/it_it/turnigy-accucel-6-80w-10a-balancer-charger-lihv-capable.html)
* 1x Turnigy Temperature Sensor for Battery Charger [(acquistato dall'Università)](https://hobbyking.com/it_it/turnigy-temperature-sensor-for-battery-charger.html)
* 1x Turnigy ignifugo LiPoly Bag Batteria (zip) (200x155x95mm) [(acquistato dall'Università)](https://hobbyking.com/it_it/fire-retardant-lipo-battery-bag-220x155x115mm-with-handle.html)
* 1x Sacco 18x22cm ai polimeri di litio ricarica Confezione [(acquistato dall'Università)](https://hobbyking.com/it_it/lithium-polymer-charge-pack-18x22cm-sack.html)
* 1x Foglio Acrilico 500 x 250 X 4 mm [(acquistato dal gruppo)](https://www.amazon.it/Sintetico-Trasparente-Lastra-500x250-spessore/dp/B00HWRE7SK/) 
* 1x Set 4 cavi TX60 [(acquistato dal gruppo)](https://www.amazon.it/gp/product/B07D71VHFG/)
* 1x Set 5 interruttori 16A 250V [(acquistato dal gruppo)](https://www.amazon.it/gp/product/B00WJLF8OQ/)
* 1x PLA BLU ELETTRICO Ø 1,75 MM 750gr Modello  1PLA60507 [(acquistato dal gruppo)](https://www.filoalfa3d.com/it/filo-175mm/8-pla-blu-elettrico-o-175-mm-8050327033504.html)
* 1x Set 20 viti e dadi 4 X 20 mm  [(acquistato dal gruppo)](https://www.leroymerlin.it/catalogo/bullone-testa-bombata-m4-x-20-mm-34445565-p?gclid=Cj0KCQiAlIXfBRCpARIsAKvManzlhvFJpEP3HyM3gSsFAGcJgsQf-8WgaicOumIYycRNrjLbfv6ho8MaApCfEALw_wcB)
* 1x Set 6 viti e dadi 6 X 50 mm [(acquistato dal gruppo)](https://www.leroymerlin.it/catalogo/bullone-testa-bombata-m6-x-50-mm-34445726-p?gclid=Cj0KCQiAlIXfBRCpARIsAKvManxFwbnbfdylts2BuHVImZX7GndCMJnq7RmF7LeRsAEqB0qyiCXRvHUaAoRLEALw_wcB)
* 1x Set 20 dadi 6 mm [(acquistato dal gruppo)](https://www.leroymerlin.it/catalogo/dado-autobloccante--m6-35746193-p?gclid=Cj0KCQiAlIXfBRCpARIsAKvManxTQPTG5XGKhWoKxlfpq0MXHgLS1shyihVZla3xUCn0OIvXjLxpkvcaAiuMEALw_wcB)
* 1x Set 30 viti e dadi [(acquistato dal gruppo)](https://www.weldom.fr/weldom/boulon-6-pans-6-8-3x10-acier-zingue-sac-30-1093856.html)

# Specifiche Software

### Specifiche richieste del Professore 
* Cambiare OS da Raspbian a [Ubuntu-Mate 16.04.2](https://ubuntu-mate.org/raspberry-pi)
* Implementare [Ros Kinetic](http://wiki.ros.org/kinetic) come Publish-Subscribe al posto MQTT 
* Implementare IA in Prolog
* Implementare Pi-camera e algoritmo per la rilevazione degli ostacoli
* Implementare voltometro

### Specifiche Aggiuntuve
* Modifica degli sketch degli arduini, standardizzazione in nodi ROS

## Funzione del Microswitch con levetta
Data la scarsa precisone nel rilevare gli ostacoli sottili, ad esempio un piede della sedia, da parte dei tre sensori ad ultrasuoni, i Microswitch con levetta risolveranno tale problema funzionando come un Bumper Sensor.  


## Lista Cartelle e descrizione contenuto

>
py_robot: cartella pricipale che contiene tutto il progetto del rover fisico
>
py_robot_v_rep: cartella che contiene tutto il progetto in versione v-rep
>
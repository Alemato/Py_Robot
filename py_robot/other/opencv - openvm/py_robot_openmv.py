# py_robot_openmv - By: alemato - mar ott 16 2018

import sensor, image, time, pyb

led = pyb.LED(3)
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.VGA)
sensor.set_windowing((240, 240))
sensor.set_auto_gain(False)
while(True):
    led.off()
    img = sensor.snapshot()
    for code in img.find_qrcodes():
        img.draw_rectangle(code.rect(), color = 127)
        print(code.payload())
        led.on()
        time.sleep(100)

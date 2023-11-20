from machine import Pin, I2C, ADC, PWM # import Pin and I2C classes
import ssd1306 # importation module ssd1306
import time

#memento pour basculer l'état de la LED
state=0
memento=1

#configuration du I2C
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
display = ssd1306.SSD1306_I2C(128, 64, i2c) # create SSD1306 object

#configuration des broches pour le joystick
VRx = ADC(Pin(26)) #La valeur X sera envoyé vers GP 26 qui controllera la teinte rouge du RGB
VRy = ADC(Pin(27)) #La valeur X sera envoyé vers GP 27 qui controllera la teinte blueue du RGB
bouton= Pin(22, Pin.IN, Pin.PULL_UP) #La valeur booléenne de l'état du bouton sera envoyé au GP 22

#configuration sorties signal PWM pour les couleurs de la LED
rouge = PWM(Pin(11))
rouge.freq(1000)
vert = PWM(Pin(12))
vert.freq(1000)
bleu = PWM(Pin(13))
bleu.freq(1000)


#Boucle du programme
while 1:
    #Basculement de l'état de la LED en appuyant sur le bouton du joystick
    if not bouton.value() and bouton.value() != memento:
        if state == 0:
            state = 1
        elif state ==1:
            state = 0
    #Conversion d'une valeur numérique vers un pourcentage
    analogx=100*(VRx.read_u16()-32767)/32767
    analogy=100*(VRy.read_u16()-32767)/32767
    if state:
        if analogx>=5:
            rouge.duty_u16(int(analogx*655))
        else:
            rouge.duty_u16(0)
       
        if analogy>=5:
            bleu.duty_u16(int(analogy*655))
        else:
            bleu.duty_u16(0)
       
        if analogx<-10 :
            vert.duty_u16(int(-analogx*655))
        elif analogy<-10 :
            vert.duty_u16(int(-analogy*655))
        else:
            vert.duty_u16(0)
    else:
        rouge.duty_u16(0)
        vert.duty_u16(0)
        bleu.duty_u16(0)
   

    memento = bouton.value()
    print("X =", analogx)
    print("Y =", analogy)
    print(" ")
    print(bouton.value())
    print("Etat =",state)


    # The following part changes according to what you want to display
    display.fill(0)
    if state: #Si la LED est allumée
        #ROUGE
        if analogx>0:
            textr="R :" +str(int(analogx))
        else:
            textr="R :0"
        #VERT
        if analogx<analogy:
            textg="G :"+str(int(-analogx))
        elif analogx > 10 and analogy > 10:
            textg="G :0"
        else:
            textg="G :"+str(int(-analogy))
           
        if analogy>0:
            textb="B :" +str(int(analogy))
        else:
            textb="B :0"
       
        display.text("LED ON", 0, 0)
        display.text(textr,0,10)
        display.text(textg,0,20)
        display.text(textb,0,30)
    else:
        display.text("LED OFF", 0, 0)
   
   
    display.show() #Afficher les données sur l'afficheur OLED
    time.sleep(0.1)

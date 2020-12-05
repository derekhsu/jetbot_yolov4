import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)  # Set Jetson Nano to use pin number when referencing GPIO pins.

GPIO.setup(33, GPIO.OUT)  # Set GPIO pin 33 (PWM2) to output mode, pin 32 is PWM1.

current_val = GPIO.HIGH
GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH)     # Set GPIO pin 11 for LED1 (RED)
GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH)     # Set GPIO pin 13 for LED2 (GREEN)
GPIO.setup(15, GPIO.OUT, initial=GPIO.HIGH)     # Set GPIO pin 15 for LED3 (BLUE)

pwm = GPIO.PWM(33, 5000) 
pwm.start(0)

# define frequency for each tone
B0  = 31
C1  = 33
CS1 = 35
D1  = 37
DS1 = 39
E1  = 41
F1  = 44
FS1 = 46
G1  = 49
GS1 = 52
A1  = 55
AS1 = 58
B1  = 62
C2  = 65
CS2 = 69
D2  = 73
DS2 = 78
E2  = 82
F2  = 87
FS2 = 93
G2  = 98
GS2 = 104
A2  = 110
AS2 = 117
B2  = 123
C3  = 131
CS3 = 139
D3  = 147
DS3 = 156
E3  = 165
F3  = 175
FS3 = 185
G3  = 196
GS3 = 208
A3  = 220
AS3 = 233
B3  = 247
C4  = 262
CS4 = 277
D4  = 294
DS4 = 311
E4  = 330
F4  = 349
FS4 = 370
G4  = 392
GS4 = 415
A4  = 440
AS4 = 466
B4  = 494
C5  = 523
CS5 = 554
D5  = 587
DS5 = 622
E5  = 659
F5  = 698
FS5 = 740
G5  = 784
GS5 = 831
A5  = 880
AS5 = 932
B5  = 988
C6  = 1047
CS6 = 1109
D6  = 1175
DS6 = 1245
E6  = 1319
F6  = 1397
FS6 = 1480
G6  = 1568
GS6 = 1661
A6  = 1760
AS6 = 1865
B6  = 1976
C7  = 2093
CS7 = 2217
D7  = 2349
DS7 = 2489
E7  = 2637
F7  = 2794
FS7 = 2960
G7  = 3136
GS7 = 3322
A7  = 3520
AS7 = 3729
B7  = 3951
C8  = 4186
CS8 = 4435
D8  = 4699
DS8 = 4978

mario_tones = [E5, E5, 0, E5, 0, C5, E5, 0, G5, 0, 0, 0, G4, 0, 0, 0, C5, 0, 0, G4, 0, 0, E4, 0, 0, A4, 0, 
  B4, 0, AS4, A4, 0, G4, E5, 0, G5, A5, 0, F5, G5, 0, E5, 0, C5, D5, B4, 0, 0, C5, 0, 0, G4, 0, 0, E4, 0, 
  0, A4, 0, B4, 0, AS4, A4, 0, G4, E5, 0, G5, A5, 0, F5, G5, 0, E5, 0, C5, D5, B4, 0, 0,
  C4, C5, A3, A4, AS3, AS4, 0, 0, 0, 0, C4, C5, A3, A4, AS3, A4, 0, 0, 0, 0, F3, F4, D3, D4, DS3, DS4, 0, 0, 0, 0, F3, F4, 
  D3, D4, DS4, DS4, 0, 0, 0, 0, DS4, CS4, D4, CS4, DS4, DS4, GS3, G3, CS4, C4, FS4, F4, E3, AS4, A4, GS4, DS4,
  B3, AS3, A3, GS3, 0, 0, 0]



# play all tone
# note = [B0, C1, CS1, D1, DS1, E1, F1, FS1, G1, GS1, A1, AS1, B1, C2, CS2, D2, DS2, E2, F2, FS2, G2, GS2, A2, AS2, B2, C3, CS3, D3, DS3, E3, F3, FS3, G3, GS3, A3, AS3, B3, C4, CS4, D4, DS4, E4, F4, FS4, G4, GS4, A4, AS4, B4, C5, CS5, D5, DS5, E5, F5, FS5, G5, GS5, A5, AS5, B5, C6, CS6, D6, DS6, E6, F6, FS6, G6, GS6, A6, AS6, B6, C7, CS7, D7, DS7, E7, F7, FS7, G7, GS7, A7, AS7, B7, C8, CS8, D8, DS8]

# play Mario Bros tone example
# source from here http://www.linuxcircle.com/2013/03/31/playing-mario-bros-tune-with-arduino-and-piezo-buzzer/

for i in mario_tones:
    if i == 0:
        pwm.ChangeDutyCycle(0)
    else:
        pwm.ChangeFrequency(i) 
        pwm.ChangeDutyCycle(30)
        GPIO.output(11, current_val)
        GPIO.output(13, current_val)
        GPIO.output(15, current_val)
        current_val ^= GPIO.HIGH
    time.sleep(0.150)

pwm.stop()                         # stop PWM
GPIO.cleanup()                     # resets GPIO ports used back to input mode


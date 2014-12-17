import sys
import tty
import termios
import time
import thread

import RPi.GPIO as GPIO
import logging
import db
import MFRC522

import MySQLdb

# Set to true if you want to use debugging
DEBUG = True

if(DEBUG):
    logging.basicConfig(format='%(asctime)s %(message)s',filename='/var/log/syslog',datefmt='%d/%m/%Y %I:%M:%S %p',level=logging.DEBUG)

# Connection with database
def connect():
    # Mysql connection setup
    return MySQLdb.connect(host="localhost", user="<user-name>", passwd="<password>", db="<database>")

# Class start
class Actions:
    incomming=1
    outcomming=2

# Prepare RFID for reading
def identity():
    reading = True
    while reading:
        MIFAREReader = MFRC522.MFRC522()

        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print("Card detected. Identifying...")

        (status,backData) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            print ("Card ID: "+str(backData[0])+""+str(backData[1])+""+str(backData[2])+""+str(backData[3])+""+str(backData[4]))
            MIFAREReader.AntennaOff()
            reading=False
            return str(backData[0])+str(backData[1])+str(backData[2])+str(backData[3])+str(backData[4])

def setGpio():
	# Show no warnings
    GPIO.setwarnings(False)
    # Use GPIO pin numbers
    GPIO.setmode(GPIO.BOARD)

# Fetch card ID
def read():
    cardId=identity()
    return cardId

     
def readNfc(action):
    # Option 1: Incomming
    if(action==49):
        print("Arrival:")
        print("Wave your card!")
        cardId=read()

        # Check if card ID is in db
        db2 = connect()
        c = db2.cursor()
        check = c.execute("SELECT *FROM cards WHERE tagId = " + cardId)

        time.sleep(1);
        
        # If card ID in db approve and authorize entry 
        if check:
            name = db.write(cardId,Actions.incomming)
            print "You can come in!"
        else:
            print "Nope, you are not one of us! Ciao!"

        logging.info("%s - Arrive",cardId)

    # Option 2 - Outcomming
    if(action==50):
        print("Going home:")
        print("Wave your card!")
        cardId=read()

        # Check if card ID is in db
        db2 = connect()
        c = db2.cursor()
        check = c.execute("SELECT *FROM cards WHERE tagId = " + cardId)

        time.sleep(1);

        # If card ID isin db approve and authorize leave
        if check:
            name = db.write(cardId,Actions.outcomming)
            print "Yup, you can leave."
        else:
            print "How did you get in here? Calling security!"

        logging.info("%s - Leaving",cardId)

    # Option 3 - Add new card user
    if(action==51):
        print("What is your name:")
        userId = raw_input('--> ')
        print("Permision level (1:Master key | 2:Guest)?")
        permission = raw_input('-->')
        print("Wave your card!")

        cardId=read()
        name = db.writeUser(userId,cardId,permission)
        print(name)

        logging.info("Created new card user: %s, Permission: %s",userId,permission)

fd = sys.stdin.fileno()
old = termios.tcgetattr(fd)

def getOneKey():
    try:
        tty.setcbreak(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        return ord(ch)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def main():

    try:
        setGpio()
        while True:
            print("=============================================")
            print("Hi Guest, please choose what you up to.")
            print("Choose option:")
            print("[1]Coming to work")
            print("[2]Going home")
            print("[3]Add new card user")
            print("=============================================")
    
            choice = getOneKey() 
            readNfc(choice)

    except KeyboardInterrupt:
        GPIO.cleanup()
        pass
    GPIO.cleanup()

if __name__ == '__main__':
    main()
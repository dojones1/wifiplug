import time
import RPi.GPIO as GPIO
from pyHS100 import SmartPlug, TPLinkSmartHomeProtocol
from pprint import pformat as pf

###### Globals

timeout=5
current_state = False
plug = None
debug = False

###### Functions

def check_state(new_state):
    if debug:
        print("Updating current_state: %d" % (new_state))
    global current_state

    if current_state:
        if new_state is False:
            print("Turning off")
            plug.turn_off()
    else:
        if new_state:
            print("Turning on")
            plug.turn_on()
    current_state = new_state

# Set up GPIO connection
GPIO_PORTS = [14, 15, 18, 23]
GPIO.setmode(GPIO.BCM)
for port in GPIO_PORTS:
    print("Setting up port: %d" % (port))
    GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_UP)

##### wait for the network to be established

##### find Plug
devToFind = 'Smart Plug 1'
devIP = ""
foundDev = False

print("Now searching for device: %s" % (devToFind))
while not foundDev:
    try:
        devs = TPLinkSmartHomeProtocol.discover(timeout=timeout)
    except IOError as e:
        if e.errno == 101:  # Network Unreachable
            devs = {}
        else:
            raise
    for devId in devs:
        alias = devId['sys_info']['system']['get_sysinfo']['alias']
        if alias == devToFind:
            devIP = devId['ip']
            foundDev = True

if foundDev:
    print("Setting up control loop with %s: %s" % (devToFind, devIP))
    plug = SmartPlug(devIP)

    check_state(False)
    
    while True:
        all_pressed = False
        portId = 0
        num_pressed = 0
        for port in GPIO_PORTS:
            circuit_open = GPIO.input(port)
            if circuit_open == False:
                num_pressed +=1
            if debug:
                print(".port %d co: %s num_pressed: %d" % (portId, str(circuit_open), num_pressed))
            portId += 1
        
        if num_pressed == len(GPIO_PORTS):
            all_pressed = True
        if debug:
            print("ap: %s  cs: %s" % (str(all_pressed), str(current_state)))
        check_state(all_pressed)
        time.sleep(0.2)

from firebase import firebase
from time import strptime, strftime, mktime, gmtime
import smbus
import time

ts = time.time()
#asd = (time.strftime("%Y-%m-%d")+time.strftime("%H:%M:%S"))
#print(asd)

firebase = firebase.FirebaseApplication('https://colordetector-7d079.firebaseio.com/')
#result = firebase.post('FYQXr86nSVg02j9XVI9TyvAvRsV2/sensordata/data1', {'rgb':'ffe1111'})
#print(result)


#CONDITION

print "Enter 1 for Gala Apple"
print "Enter 2 for Green Apple"
print "Enter 3 for Golden Apple"
print "Enter 4 for Cavendish Banana"
print "Enter 5 for Plantain Banana"
print "Enter 6 for Green Banana"
print "Enter 7 for Orange"

switch = {
	'1': "Gala Apple",
	'2': "Green Apple",
	'3': "Golden Apple",
        '4': "Cavendish Banana",
        '5': "Plantain Banana",
        '6': "Green Banana",
        '7': "Orange"
        }
inp = input('Please enter the fruit you want: ')
#print('Result : ', switch.get(str(inp)))
firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/sensordata/data1', 'fruitname', str(switch.get(str(inp))))
#TCS34725
bus = smbus.SMBus(1)
# I2C address 0x29
# Register 0x12 has device ver. 
# Register addresses must be OR'ed with 0x80
bus.write_byte(0x29,0x80|0x12)
ver = bus.read_byte(0x29)
# version # should be 0x44
if ver == 0x44:
 print "Device found\n"
 bus.write_byte(0x29, 0x80|0x00) # 0x00 = ENABLE register
 bus.write_byte(0x29, 0x01|0x02) # 0x01 = Power on, 0x02 RGB sensors enabled
 bus.write_byte(0x29, 0x80|0x14) # Reading results start register 14, LSB then MSB


# Ads1115
# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Ads1115
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Ads1115
# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
adc = Adafruit_ADS1x15.ADS1115(address=0x4B, busnum=1)

# Ads1115
# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1


#Tmp007
# Get I2C bus
bus = smbus.SMBus(1)

# TMP007 address, 0x40(64)
# Select configuration register, 0x02(02)
#		0x1540(5440)	Continuous Conversion mode, Comparator mode


while True:
	
	data = [0x1540]
        bus.write_i2c_block_data(0x40, 0x02, data)


	data = bus.read_i2c_block_data(0x40, 0x03, 2)
	data = bus.read_i2c_block_data(0x29, 0)
#Color sensor
	clear = clear = data[1] << 8 | data[0]
  	red = data[3] << 8 | data[2]
	
  	green = data[5] << 8 | data[4]
	
  	blue = data[7] << 8 | data[6]
	
  	#crgb = "C: %s, R: %s, G: %s, B: %s\n" % (clear, red, green, blue)
	val = (red << 16) + (green << 8) + blue
	print "%s" % (hex(val) [3:]).upper()
  	#print crgb
  	time.sleep(1)
	data = bus.read_i2c_block_data(0x40, 0x03, 2)
	firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/sensordata/data1', 'rgb', str(hex(val) [3:]))
	firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/sensordata/data1', 'timestamp', str(int(ts)))


# Convert the data to 14-bits
        cTemp = ((data[0] * 256 + (data[1] & 0xFC)) / 4)
        if cTemp > 8191 :
        	cTemp -= 16384
        cTemp = cTemp * 0.03125
        fTemp = cTemp * 1.8 + 32
	

    	values = [0]*1
    	for i in range(1):
        # Read the specified ADC channel using the previously set gain value.
        #values[i] = adc.read_adc(i, gain=GAIN)
        	bitValue = 32768
        	voltageValue = 2.048/bitValue
        	values[i] = (((adc.read_adc(i, gain=GAIN))*voltageValue)*4.096)
# TMP007 address, 0x40(64)
# Read data back from 0x03(03), 2 bytes
# cTemp MSB, cTemp LSB

# Output data to screen

        print "Object Temperature in Celsius : %.2f C" %cTemp
        print "Object Temperature in Fahrenheit : %.2f F" %fTemp
	
	

	tempts = {'temp':cTemp,
		'timestamp':ts}

	
	firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/temperature/data1', 'temp', str(cTemp))
	firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/temperature/data1', 'timestamp', str(int(ts)))

	time.sleep(0.5)


    	if(values[i] < 1.29):
        	print ("Default 0v/Not Connected\n")
    	else:
        	print('|(A0) Voltage input: {0:>6}v| '.format(*values))

		voltts = {'Volt':values[i],
		'timestamp':ts}

	  	firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/Voltage/data1', 'volt', str(values[i]))
		firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/data/data1', 'volt', str(values[i]))
		firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/data/data1', 'timestamp', str(int(ts)))
		firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/Battery/data1', 'timestamp', str(int(ts)))
		firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/graph/data1', 'timestamp', str(int(ts)))
		firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/graph/data2', 'timestamp', str(int(ts)))
		firebase.put('FYQXr86nSVg02j9XVI9TyvAvRsV2/graph/data3', 'timestamp', str(int(ts)))


		time.sleep(2.5)

        	time.sleep(0.5)

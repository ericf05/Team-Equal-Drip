import smbus
import math
from time import sleep

BH1750_ADDR = 0x77

class BMP180:
	address = BH1750_ADDR
	bus = smbus.SMBus(1)
	mode = 1
	
	CONTROL_REG = 0xF4
	DATA_REG = 0xF6
	
	CAL_AC1_REG = 0xAA
	CAL_AC2_REG = 0xAC
	CAL_AC3_REG = 0xAE
	CAL_AC4_REG = 0xB0
	CAL_AC5_REG = 0xB2
	CAL_AC6_REG = 0xB4
	CAL_B1_REG = 0xB6
	CAL_B2_REG = 0xB8
	CAL_MB_REG = 0xBA
	CAL_MC_REG = 0xBC
	CAL_MD_REG = 0xBE
	
	calAC1 = 0
	calAC2 = 0
	calAC3 = 0
	calAC4 = 0
	calAC5 = 0
	calAC6 = 0
	calB1 = 0
	calB2 = 0
	calMB = 0
	calMC = 0
	calMD = 0
	
	def __init__(self):
		self.read_calibration_data()
	
	def read_signed_16_bit(self, register):
		msb = self.bus.read_byte_data(self.address, register)
		lsb = self.bus.read_byte_data(self.address, register+1)
		
		if msb > 127:
			msb -= 256
			
		return (msb << 8) + lsb
		
	def read_unsigned_16_bit(self, register):
		msb = self.bus.read_byte_data(self.address, register)
		lsb = self.bus.read_byte_data(self.address, register+1)
		
		return (msb << 8) + lsb
		
	def read_calibration_data(self):
		self.calAC1 = self.read_signed_16_bit(self.CAL_AC1_REG)
		self.calAC2 = self.read_signed_16_bit(self.CAL_AC2_REG)
		self.calAC3 = self.read_signed_16_bit(self.CAL_AC3_REG)
		self.calAC4 = self.read_signed_16_bit(self.CAL_AC4_REG)
		self.calAC5 = self.read_signed_16_bit(self.CAL_AC5_REG)
		self.calAC6 = self.read_signed_16_bit(self.CAL_AC6_REG)
		self.calB1 = self.read_signed_16_bit(self.CAL_B1_REG)
		self.calB2 = self.read_signed_16_bit(self.CAL_B2_REG)
		self.calMB = self.read_signed_16_bit(self.CAL_MB_REG)
		self.calMC = self.read_signed_16_bit(self.CAL_MC_REG)
		self.calMD = self.read_signed_16_bit(self.CAL_MD_REG)
		
	def get_raw_temp(self):
		self.bus.write_byte_data(self.address, self.CONTROL_REG, 0x2E)
		
		sleep(0.5)
		
		raw_data = self.read_unsigned_16_bit(self.DATA_REG)
		
		return raw_data
		
	def temperature(self):
		UT = self.get_raw_temp()
		
		X1 = 0
		X2 = 0
		B5 = 0
		temp = 0.0
		
		X1 = ((UT - self.calAC6) * self.calAC5) / math.pow(2, 15)
		X2 = (self.calMC * math.pow(2, 11)) / (X1 + self.calMD)
		B5 = X1 + X2
		temp = ((B5 + 8) / math.pow(2, 4)) / 10
		
		return temp
		
def main():
	try:
		obj = BMP180()
		Celcius = round(obj.temperature(), 2)
		Fahren = round((Celcius * 1.8) + 32, 2)
		return Fahren
	except FileNotFoundError:
		print('ERROR: Please enable I2C')
	except OSError:
		print('ERROR: check wiring')
	except Exception as error:
		print('ERROR: Unknown error', error)
		
if __name__ == "__main__":
	print(main())
			
	
	

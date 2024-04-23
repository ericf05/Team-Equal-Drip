import time
import smbus

BH1750_ADDR = 0x23
CMD_READ = 0x10

class BH1750(object):

	def __init__(self):
		self.bus = smbus.SMBus(1)
		
	def light(self):
		data = self.bus.read_i2c_block_data(BH1750_ADDR, CMD_READ)
		result = (data[1] + (256 * data[0])) / 1.2
		return format(result, '.0f')

def main():
	try:
		obj = BH1750()
		# print('Light: ' + obj.light() + ' Lux')
		return obj.light()
	except Exception as error:
		print('ERROR: ' + str(error))

if __name__ == "__main__":
	print(main())

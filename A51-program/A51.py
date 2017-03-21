import sys
import copy

def testBit(int_type, offset,size):
	offset = offset - (size - int_type.bit_length())
	if(offset < 0):
		return 0
	mask = 1 << offset
	
	val =  (int_type & mask)
	
	if val:
		return val >> (val.bit_length() - 1)
	else:
		return val





def xorOffsets(int_type,offset,size,key,key_offeset):
	res = 0
	val = copy.deepcopy(int_type)
	for i in offset:

		
		i = (size-(i + 1))
		

		res ^= testBit(val,i,val.bit_length())
	res ^= testBit(key,key_offeset,key.bit_length())
	return res


def LSFR(data,offset,size,key,key_offeset):
	#print(bin(data))
	xorVal = xorOffsets(data,offset,size,key,key_offeset)
	#print(bin(data))
	#print(xorVal)
	dataLen = data.bit_length()
	
	xorVal <<= (size - 1)
	
	
	#lsb = data & 1
	data >>= 1 
	#print(bin(data))
	data = data | xorVal
	#print(bin(data))
	return data
	#return(lsb)
	
def intializeKey(data,offset,data_size,key,key_size):
	for i in range(0,key_size):
		pass

		data = LSFR(data,offset,data_size,key,(key_size - (i + 1)))
		if(i == (key_size - 1)):
			return data


def findMajorityBit(data1,data2,data3):
	return ((testBit(data1,8,19) & testBit(data2,10,22)) | (testBit(data1,8,19) & testBit(data3,10,23)) | (testBit(data2,10,22) & testBit(data3,10,23)) )


R1 = R2 = R3 = 0

key = int(5633806854350474042)

data1 = int(R1)

data2 = int(R2)

data3 = int(R3)
data1 = intializeKey(data1,[13,16,17,18],19,key,64)
data2 = intializeKey(data2,[20,21],22,key,64)

data3 = intializeKey(data3,[7,20,21,22],23,key,64)
print(bin(data1))
print(bin(data2))
print(bin(data3))

#step 2
#frameCounter = 1110101011001111001011
frameCounter = int(3847115)

data1 = intializeKey(data1,[13,16,17,18],19,frameCounter,22)
data2 = intializeKey(data2,[20,21],22,frameCounter,22)
data3 = intializeKey(data3,[7,20,21,22],23,frameCounter,22)

print(bin(data1))
print(bin(data2))
print(bin(data3))

#step 3

majorityBit = findMajorityBit(data1,data2,data3)
print(majorityBit)

for i in range(0,100):
	pass
	#print(i)
	majorityBit = findMajorityBit(data1,data2,data3)
	#print(majorityBit)

	if(majorityBit == (testBit(data1,8,19))):
		#print("1 active")
		data1 = LSFR(data1,[13,16,17,18],19,0,1)

	if(majorityBit == (testBit(data2,10,22))):
		#print("2 active")
		data2 = LSFR(data2,[20,21],22,0,1)

	if(majorityBit == (testBit(data3,10,23))):
		#print("3 active")
		data3 = LSFR(data3,[7,20,21,22],23,0,1)


print(bin(data1))
print(bin(data2))
print(bin(data3))

#step 4 generate the key stream

finalKeyStr = ""
finalKey = 0
for i in range(0,228):
	lastBitXor = ((data1 & 1) ^ (data2 & 1) ^ (data3 & 1))
	finalKey = finalKey << 1
	finalKey = finalKey | lastBitXor
	
	finalKeyStr = finalKeyStr + str(lastBitXor)
	majorityBit = findMajorityBit(data1,data2,data3)

	if(majorityBit == (testBit(data1,8,19))):
		#print("1 active")
		data1 = LSFR(data1,[13,16,17,18],19,0,1)

	if(majorityBit == (testBit(data2,10,22))):
		#print("2 active")
		data2 = LSFR(data2,[20,21],22,0,1)

	if(majorityBit == (testBit(data3,10,23))):
		#print("3 active")
		data3 = LSFR(data3,[7,20,21,22],23,0,1)

plainText = int(sys.argv[1])
print((finalKeyStr))
print(bin(finalKey))

encryptedText = finalKey ^ plainText
print(bin(encryptedText))
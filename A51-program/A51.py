import sys
import copy
#Function to test a particular bit of a given int_type is 0 or 1
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




#Function to do xor of a register with a given stream for given offsets
def xorOffsets(int_type,offset,size,key,key_offeset):
	res = 0
	val = copy.deepcopy(int_type)
	for i in offset:

		
		i = (size-(i + 1))
		

		res ^= testBit(val,i,val.bit_length())
	res ^= testBit(key,key_offeset,key.bit_length())
	return res

#Function to implement the working for linear feedback shift register
def LSFR(data,offset,size,key,key_offeset):
	
	xorVal = xorOffsets(data,offset,size,key,key_offeset)
	
	dataLen = data.bit_length()
	
	xorVal <<= (size - 1)
	
	
	#Right shift the register 1 bit
	data >>= 1 
	
	#put the xor value at the MSB of the register
	data = data | xorVal
	
	return data
	
#Function to put a key or any stream in the register bit by bit by xoring the given offsets
def intializeKey(data,offset,data_size,key,key_size):

	for i in range(0,key_size):
		pass

		data = LSFR(data,offset,data_size,key,(key_size - (i + 1)))
		if(i == (key_size - 1)):
			return data

#Finding the majority bits from the three registers
def findMajorityBit(data1,data2,data3):
	return ((testBit(data1,8,19) & testBit(data2,10,22)) | (testBit(data1,8,19) & testBit(data3,10,23)) | (testBit(data2,10,22) & testBit(data3,10,23)) )


R1 = R2 = R3 = 0

#The seed value which is used
key = int(5633806854350474042)

#Initializing three registers
data1 = int(R1)

data2 = int(R2)

data3 = int(R3)

#step 1
#Initializing the 64 bit seed in three registers
data1 = intializeKey(data1,[13,16,17,18],19,key,64)
data2 = intializeKey(data2,[20,21],22,key,64)
data3 = intializeKey(data3,[7,20,21,22],23,key,64)


#step 2
#frameCounter = 1110101011001111001011
frameCounter = int(3847115)

#intializing 22 bits frame counter in three registers
data1 = intializeKey(data1,[13,16,17,18],19,frameCounter,22)
data2 = intializeKey(data2,[20,21],22,frameCounter,22)
data3 = intializeKey(data3,[7,20,21,22],23,frameCounter,22)



#step 3

#Finding majority bit from three registers
majorityBit = findMajorityBit(data1,data2,data3)

#Clocking the registers for 100 iterations if the majority bit is same as the offset bit of that register
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




#step 4 generate the key stream

finalKeyStr = ""
finalKey = 0
fileName = sys.argv[1]
with open(fileName, 'r') as myfile:
    plainText = myfile.read()


plainTextByte = str.encode(plainText)
plainText = int.from_bytes(plainTextByte,byteorder = sys.byteorder)
fileLen = plainText.bit_length()

#Generating the key stream for a given file length
for i in range(0,fileLen):
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

print("Generated key is:")
print((finalKeyStr))
print("\n")

print("File content is:")
print(plainTextByte)
print("\n")







encryptedText = finalKey ^ plainText
byteEncryptedText =  encryptedText.to_bytes((encryptedText.bit_length() // 8) + 1, byteorder = sys.byteorder)

print("Encrypted plain text value is:")
print((byteEncryptedText))
print("\n")

decrypt = encryptedText ^ finalKey
byteDecryptedText = decrypt.to_bytes((decrypt.bit_length() // 8) + 1, byteorder = sys.byteorder)

print("Decrypted plain text value is:")
print(byteDecryptedText)
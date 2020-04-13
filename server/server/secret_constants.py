import os
from hashlib import md5
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes 
from cryptography import utils
from cryptography.hazmat.backends.interfaces import CipherBackend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes, hmac

#current working directory for ease
cwd = os.getcwd()
print(cwd)
print(os.listdir(cwd))

#create filepath to file in cwd
filepath = '57462745357__FD26E96B-D977-4CA1-A97E-9406637B409C.jpg'


def MyEncryptMAC(message, EncKey, HMACKey):

	#create initial vector and padd the message
	iv = os.urandom(16)
	padder = padding.PKCS7(128).padder()
	message = padder.update(message)
	message += padder.finalize()
	backend = default_backend()

	#make the cipher and encrypt
	cipher = Cipher(algorithms.AES(EncKey), modes.CBC(iv), backend=backend)
	encryptor = cipher.encryptor()
	c = encryptor.update(message) + encryptor.finalize()

	#Make the HMACKey tag and add onto the cipher text
	tag = hmac.HMAC(HMACKey, hashes.SHA256(), backend=default_backend())
	tag.update(c)
	tag = tag.finalize()
	return c, iv, tag

def MyFileEncryptMAC(filepath):

	#create pseudo random key and HMACkey
	EncKey = os.urandom(32)
	HMACKey = os.urandom(32)

	#open the file
	#fr = open(filepath, "rwx")
	message = "secret key"
	#fr.close()
	
	(c, iv, tag) = MyEncryptMAC(message, EncKey, HMACKey)

	#write cipher back to file and close
	ext = filepath
	file = open(filepath, "wb")
	file.write(c)
	file.close()
	return c, iv, tag, EncKey, ext, HMACKey

def MyDecryptMAC(c, tag, HMACKey, iv, EncKey):
	#create new htag and verify that they're equal
	hTag = hmac.HMAC(HMACKey, hashes.SHA256(), backend=default_backend())
	hTag.update(c)
	hTag.verify(tag)

	backend = default_backend()
	cipher = Cipher(algorithms.AES(EncKey), modes.CBC(iv), backend=backend)
	decryptor = cipher.decryptor()
	newMessage = decryptor.update(c) + decryptor.finalize()
	return newMessage

def MyFileDecryptMAC(c, tag, filepath, HMACKey, iv, EncKey):
	file = open(filepath, "wb")
	(newMessage) = MyDecryptMAC(c, tag, HMACKey, iv, EncKey)
	file.write(newMessage)
	file.close()
	return newMessage

def makeKey():
	(c, iv, tag, EncKey, ext, HMACKey) = MyFileEncryptMAC(filepath)
	print(c)
	secretkey = MyFileDecryptMAC(c, tag, ext, HMACKey, iv, EncKey)
	return str(HMACKey)
  
from PIL import Image                                                              #Importing image function from Python Image Library
import binascii                                                                    # Enables Binary to ASCII conversion and vice-versa

def rgb2hex(r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)                               #Converts RGB values of the pixels to Hexadecimal form and also appends a '#' to the front

def hex2rgb(hexcode):
        return tuple(map(ord, hexcode[1:].decode('hex')))                          #Returns the Hexafied RGB components in the form of a tuple

def str2bin(message):
        binary = bin(int(binascii.hexlify(message), 16))
        return binary[2:]                                                                  #Strip '0b' from the binary

def bin2str(binary):
        message = binascii.unhexlify('%x' % (int('0b' + binary, 2)))
        return message

def encode(hexcode, digit):
        if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):				#If the last value of the blue pixel lies in range
                hexcode = hexcode[:-1] + digit						 #Replace with message bit
                return hexcode								 #Return modified pixel info
        else:
                return None

def decode(hexcode):
        if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
                return hexcode[-1]
        else:
                return None

def hide(filename, message):
        img = Image.open(filename)
        binary = str2bin(message) + '1111111111111110'

        if img.mode in ('RGBA'):
                img = img.convert('RGBA')
                datas = img.getdata()

                newData = []
                digit = 0
                for item in datas:
                        if (digit < len(binary)):
                                newpix = encode(rgb2hex(item[0], item[1], item[2]), binary[digit])
                                if newpix == None:
                                        newData.append(item)
                                else:
                                        r,g,b = hex2rgb(newpix)
                                        newData.append((r,g,b,255))
                                        digit += 1
                        else:
                                newData.append(item)
                img.putdata(newData)
                img.save(filename[:-4] + '2.png', "PNG")

                return "\n\n Completed !!! Your message was successfully encrypted into " + filename[:-4] + '2.png'
        return " ***** Incorrect Image Mode was opened and we weren't able to encrypt your message. ******"

def retr(filename):
        img = Image.open(filename)
        binary = ''

        if img.mode in ('RGBA'):
                img = img.convert('RGBA')
                datas = img.getdata()

                for item in datas:
                        digit = decode(rgb2hex(item[0], item[1], item[2]))
                        if digit == None:
                                pass
                        else:
                                binary = binary + digit

                                if (binary[-16:] == '1111111111111110'):
                                        print ("\n Success !!! Data found...\n Message Decrypted is...\n ~~~~~~~~~~~~~~~~~~~~~~~\n\n")
                                        return bin2str(binary[:-16])
                return bin2str(binary)
        return "\n ***** Incorrect Image Mode was opened and we weren't able to decrypt your message *****"

def Main():
        print ("\n\n\t\t\t ***** STEGANOGRAPHY PROJECT *****")
        print ("\t\t\t ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("\n\n Image steganograaphy is the art of encrypting messages into image files. \n This project implements the same concept.")
        print ("\n\n Please select a valid option.\n")
        print (" 1. ENCRYPT - This will hide your image in the picture you provide.")
        print (" 2. DECRYPT - This will decode the message you have encrypted in the image you provide.\n\n")
        choice = input(" Please choose a valid option (1/2): ")

        if choice == '1':
                message = input(" Please enter your message: ")
                filename = input(" Please select the image in which you wish to encrypt this information: ")
                action = hide(filename, message)
                print (action)
        elif choice == '2':
                filename = input(" Please select the image from which you wish to decrypt the information: ")
                message = retr(filename)
                print (" " + message)
        else:
                print ("You did not select a valid option!!! The program will now terminate!")
        
if __name__ == '__main__':
        Main()

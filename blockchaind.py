#!/usr/bin/env python
import datetime
import hashlib
import os
import pickle
import base64
import rsa
import sys
testmode=True
useless=False
# Time stuff - Just for redability these are defined.. completely useless use for functions
def strtotimestamp(date):
    return datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f")
# END Time stuff

# Block chain skelliton code
def create_transaction(sender_pub,sender_priv,reciever,metadata,data):
    transaction={"SENDER":sender_pub,"RECIEVER":reciever,"TIMESTAMP":str(datetime.datetime.now()),"METADATA":metadata,"DATA":data}
    transaction_encoded=pickle.dumps(transaction)
    privkey = rsa.PrivateKey.load_pkcs1(base64.decodebytes(sender_priv),"DER")
    signature=rsa.sign(transaction_encoded,privkey,hash_method="SHA-256")
    transaction={"TRANSACTION":transaction,"SIGNATURE":signature}
    return transaction
def check_transaction(sender_pub,transaction):
    publickey = rsa.PublicKey.load_pkcs1(base64.decodebytes(sender_public),"DER")
    if(rsa.verify(pickle.dumps(transaction["TRANSACTION"]),transaction["SIGNATURE"],publickey)):
        return True
    else:
        return False
def create_block(header,transaction: list,transaction_counter): #Miner code so need miner signature..
    block={"HEADER":header,"TRANSACTION":transaction,"TRANSACTION_COUNTER":transaction_counter}
    return block
def create_block_header(id,version,previous_block_hash,merkle_root_hash,timestamp,difficulty,nonce):
    block_header={"ID":id,"VERSION":version,"PREVIOUS_BLOCK_HASH":previous_block_hash,"MERKLE_ROOT_HASH":merkle_root_hash,"TIMESTAMP":timestamp,"DIFFICULTY":difficulty,"NONCE":nonce}
    return block_header
# END Block chain skelliton

#Block disk interface
def saveBlock(block,N=False): # N means dont do anything just show what it might do.
    stats={"current":-1,"hash":0,"block_count":0,"last_transaction":0}
    if(not os.path.exists("blockchain/stats")):
        if(not os.path.exists("blockchain")):
            os.mkdir("blockchain")
        f=open("blockchain/stats","wb")
    else:
        f=open("blockchain/stats","rb")
        try:
            stats=pickle.loads(f.read())
        except:
            print("Error loads blockchain/stats, file appears to be corrupt")
        f.close()
        f=open("blockchain/stats","wb")
    nexthash=str(hashlib.sha256(pickle.dumps(block)).hexdigest())
    nextcount=stats["block_count"]+1
    nextcurrent=block["HEADER"]["ID"]
    if(N):
        print({"hash":nexthash,"count":nextcount,"current":nextcurrent})
    else:
        stats={"current":nextcurrent,"hash":nexthash,"block_count":nextcount,"last_transaction":stats["last_transaction"]}
        if(nextcurrent==0):
            stats["block_count"]=1 # Genesis block
        f.write(pickle.dumps(stats))
        f.close()
        f=open("blockchain/block_"+str(nextcurrent),"wb")
        f.write(pickle.dumps([block,nexthash]))
def loadBlockAndVerify(blockid):
    if(not os.path.exists("blockchain/block_"+str(blockid))):
        raise ValueError("Block not avaiable")
    else:
        f=open("blockchain/block_"+str(blockid),"rb")
        block,hash = pickle.loads(f.read())
        newhash = str(hashlib.sha256(pickle.dumps(block)).hexdigest())
        if(newhash == hash):
            return block

# END Block disk interface

def mine(transaction: list,difficulty="1fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",show_mining=False):
    id=0
    if(os.path.exists("blockchain/stats")):
        f=open("blockchain/stats","rb")
        stats = pickle.loads(f.read())
        id=stats["current"]+1
        f.close()
    version=0
    previous_block_hash=0
    merkle_root_hash=0
    timestamp=str(datetime.datetime.now())
    transaction_counter=1
    nonce=0
    if(id!=0):
        if(os.path.exists("blockchain/block_"+str(id-1))):
            f=open("blockchain/block_"+str(id-1),"rb")
            previous_block_hash = pickle.loads(f.read())[-1]
        else:
            print("Miner:Cannot find previous block!")
    print("Started mining block",id)
    while(True):
        block=create_block(header=create_block_header(id=id,version=version,previous_block_hash=previous_block_hash,
                    merkle_root_hash=merkle_root_hash,timestamp=timestamp,difficulty=difficulty,
                    nonce=nonce),transaction=transaction,transaction_counter=transaction_counter)
        hash=str(hashlib.sha256(pickle.dumps(block)).hexdigest())
        if(show_mining):
            print(int(hash,16),int(difficulty,16))
        if(int(hash,16)<int(difficulty,16)):
            if(show_mining):
                print("Succefully mined block "+str(id))
                print("Hash:",hash)
            break
        nonce+=1
    print(hash)
    return block
def fileToMeta_Data(filename):
    f=open(filename,"rb")
    data=f.read()
    metadata={"LENGTH":len(data),"FILENAME":filename.split("/")[-1]}
    return metadata,data

sender_private = b'MIICYAIBAAKBgQDCmg8eXbWUMfTJLrEGtu4ZnmpZEdtAgzLyoapbdnfIEARHye9ZETScrCX4sT0FJGcjrKiHQtSobau7NPIgDWw9kU3UpUekNRVSf0roOAQg84slJoRBI1f34l9NBjgms1gkCB6FqsnVD3OgTcErMaUL8hDsXPYsnKNnhZP5IrHh+wIDAQABAoGAenbvSsHYUoG5tZ3fpAUdBBxQeusk2o12U4Dvr413RfzmZLMtIBUW0f34C3CmoQTOr4GpsS2anMAf0bk4mGZOcMyuY8cEl2O5oUfm03LOxGoR2bw3/v/g0aPWIxJFulD6aCvAYhuUSngAZyLVJSIu3hsUqBB/Oye9YVyVxk/LEekCRQDbZwE/cP6stykxYfLbuGDsxwzbK8VUSbniJPAJmpHj3Lsh5RgddfQ+KXgRuiy4WTM3Wa2e5/VgVaxKR4W/7O+m7U6tJQI9AOMQAwD20fygTfNC6342OWVnoO8mSH+8TC/3WbgumxmW2dYpFAwWLAgtUDEs1VrVdSpEaUkfWa6pro94nwJEAWSF/YEaHL6M5GNax0pEUzxwOHPurLpLE8RoQadZhbjA91Yc8RLumfZpbLNh1Um7qX5IO9n9FL92eII7txwp6UVYWoECPGW5ua7H5WHJq8KNO5XK00IEAEzEGPzpLjTbGx3x+1imhad1td6IXGe5bVDqphdQxHIQPh8dZX9j06nBPwJFAKbIwDdJS3Zc/i/Gz3u8cDcX+a/HP6XVcmBfIQmJnqnfh+CX67nDI9s51kGzB8Qhw2TQtW8ifCKCUFXEhd/IoqYVVu6L'
sender_public = b'MIGJAoGBAMKaDx5dtZQx9MkusQa27hmealkR20CDMvKhqlt2d8gQBEfJ71kRNJysJfixPQUkZyOsqIdC1Khtq7s08iANbD2RTdSlR6Q1FVJ/Sug4BCDziyUmhEEjV/fiX00GOCazWCQIHoWqydUPc6BNwSsxpQvyEOxc9iyco2eFk/kiseH7AgMBAAE='
reciever_public = b'MIGJAoGBAMzzGN/1Ohd2g8t7EiRj5PARxVVhMrEH9WPz82Up2lxiNMN12LUXt+YaQ1kE2jRmCZi9gClmf1v1+p6pvKZAWRSVSTDzcpavfVwP+VqhED22JrwyMqOZbMBHLwIeaBWSdajhpcXTxMnWdPnCywGAKW2JBggEDpT3OK9yOEWq4XnJAgMBAAE='
reciever_private = b'MIICXwIBAAKBgQDM8xjf9ToXdoPLexIkY+TwEcVVYTKxB/Vj8/NlKdpcYjTDddi1F7fmGkNZBNo0ZgmYvYApZn9b9fqeqbymQFkUlUkw83KWr31cD/laoRA9tia8MjKjmWzARy8CHmgVknWo4aXF08TJ1nT5wssBgCltiQYIBA6U9zivcjhFquF5yQIDAQABAoGAOBMPLD+BLGg9uQ+sMA6w1cpW7nxQjUU7K6TUZEpmNz6bZxs4NpwNscRfxtxgA1QjrgmzJiCoGfYcIwsXnLbJF+5ybPk13Qu3MvAzyljLlhtmxKUy2VyUu4nncfHIpCeHiCrRcJ2uzbpnc0hlL34ZCTe3vbejPPud21Z+h3liQwECRQDPcu8XpR0rWxG3YdfO96ov9Q6RXqnHdt35PSLy9yCoUDqAklw3h+FaR3FCe4S4lQCSiNLxecSPdOnH6/DGHhuQHp2yoQI9APzqarJgdaCUjkEbaqZJfpbqs1kIpyVLyDsA1O4sdZlBM3I/MlFp6chvsLPEBNkzPTkmqZ1UwfJV7BEeKQJEK2J0ElPbt9eB6wIxaf1twD3V4B0WELsRTTC2AG4ijFDLC1yQoKRwQrsyOp8ucJPo3Lx0sT+wFfhzc/YqEqT1Sry8akECPGv2hWVv18aco70XPweNCATUW4r+Lpu1JdxKFps1T14Efzmd0JUAaVOumfejDY7KWLA02OLYc5JHK2aDQQJEeuddtBwpCQshahPI9RdwLTDnfcF9ysp2f5KqcuvIwOVL6mOT/WmRNH2DAL3/LaoHYuYSugTMNRNaL2edqJ1V+dj9rcc='


# # block=create_block(header=create_block_header(id=0,version=0,previous_block_hash=0,
# #                    merkle_root_hash=0,timestamp=str(datetime.datetime.now()),difficulty=0,
# #                    nonce=0),transaction=[create_transaction(sender_pub=sender_public,
# #                    sender_priv=sender_private,reciever=1,metadata=b"some metadata",
# #                    data=b"some data")],transaction_counter=1)
if(len(sys.argv)>1):
    if(sys.argv[1]=="--reset" or sys.argv[1]=="-r" or sys.argv[1]=="--test" or sys.argv[1]=="-t"):
        print("TEST MODE")
    else:
        testmode=False
if(len(sys.argv)>1):
    start=True
    for i in sys.argv:
        if(start):
            start=False
            continue
        if(i=="--less" or i=="-l"):
            useless=True
            
if(testmode):
    os.system("rm -rf blockchain")
# metadata,data=fileToMeta_Data("testfile/Bitcoin - A Peer-to-Peer Electronic Cash System White Paper.pdf")
# block = mine([create_transaction(sender_pub=sender_public,sender_priv=sender_private,
#               reciever=1,metadata=metadata,data=data)],show_mining=True)
# saveBlock(block)
# if(loadBlockAndVerify(0)==block):
#     print("Verified! 0")
# print("Checking transaction:",check_transaction(sender_public, block["TRANSACTION"][0]))
# metadata,data=fileToMeta_Data("testfile/7104822.png")
# block = mine([create_transaction(sender_pub=sender_public,sender_priv=sender_private,
#               reciever=1,metadata=metadata,data=data)],show_mining=True)
# saveBlock(block)
# if(loadBlockAndVerify(1)==block):
#     print("Verified! 1")


# Begin UI STUFF

print("Copyleft 🄯 2021 Abhiram Shibu, Aishwarya Venugopal")
print("This program comes with NO WARRANTY and should ONLY be used FOR ACADEMIC PURPOSE!")
print('''This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA''')
transactions=[]
def main():
    global transactions
    global sender_public
    global sender_private
    global reciever_private
    global reciever_public
    print("Demo MENU")
    print("t) Add Transaction")
    print("m) Mine")
    print("d) Debug")
    print("e) Exit")
    c=input("Enter an option from above:")
    if(c[0].lower()=='t' or c[0]=='1'):
        filename=input("Drag and drop or enter the path to file (d/?):").replace("'","")
        private_sender = input("Enter private key of sender (d/?):")
        public_sender = input("Enter public key of sender (d/?):")
        public_receiver = input("Enter public key of receiver (d/?):")
        if(len(filename)==1 and filename[0].lower()=="d"):
            filename="testfile/Bitcoin - A Peer-to-Peer Electronic Cash System White Paper.pdf"
        while(True):
            if(not os.path.exists(filename)):
                filename=input("Drag and drop or enter the path to file (d/?):").replace("'","")
            else:
                break
        if(len(filename)==1 and filename[0].lower()=="d"):
            filename="testfile/Bitcoin - A Peer-to-Peer Electronic Cash System White Paper.pdf"
        if(not(len(private_sender)==1 and private_sender[0].lower()=="d")):
            sender_private=private_sender
        if(not(len(public_sender)==1 and public_sender[0].lower()=="d")):
            sender_public=public_sender
        if(not(len(public_receiver)==1 and public_receiver[0].lower()=="d")):
            reciever_public=public_receiver       
        metadata,data=fileToMeta_Data(filename)
        transactions.append(create_transaction(sender_pub=sender_public,sender_priv=sender_private,reciever=reciever_public,metadata=metadata,data=data))
    elif(c[0].lower()=='m' or c[0]=='2'):
        print("Creating block by mining")
        block = mine(transactions,show_mining=True)
        print("Saving to disk")
        saveBlock(block)
        if(loadBlockAndVerify(block["HEADER"]["ID"])==block):
            print("Verified!",block["HEADER"]["ID"])
        transactions=[]
    elif(c[0].lower()=='d' or c[0]=='3'):
        blockdump=True
        statsdump=True
        if(os.path.exists("dumpblock.py")):
            print("BlockDumper module is found, adding")
        else:
            print("Warning: BlockDumper is missing, try adding manually")
            blockdump=False
        if(os.path.exists("dumpstats.py")):
            print("StatsDumper module is found, adding")
        else:
            print("Warning: StatDumper is missing, try adding manually")
            statsdump=False
        print("Debugging console menu")
        if(blockdump):
            print("b) DUMP BLOCK")
        if(statsdump):
            print("s) DUMP STATS")
        choice = input("Enter a choice:")
        if(choice=="b"):
            if(not os.path.exists("blockchain/stats")):
                print("ERROR: No blockchain or stats found!")
            else:
                f=open("blockchain/stats","rb")
                stats = pickle.loads(f.read())
                f.close()
                nblocks=stats["block_count"]
                choice = input("Enter block id (valid 0-"+str(nblocks)+"):")
                if(os.path.exists("blockchain/block_"+str(choice))):
                    if(not useless):
                        os.system("python dumpblock.py blockchain/block_"+str(choice))
                    else:
                        os.system("python dumpblock.py blockchain/block_"+str(choice)+"|less")
        elif(choice=="s"):
            if(not os.path.exists("blockchain/stats")):
                print("ERROR: No blockchain or stats found!")
            else:
                os.system("python dumpstats.py")
    elif(c[0].lower()=='e' or c[0]=='4'):
        print("Exiting gracefully..")
        return 1
    return 0
try:
    while(True):
        if(main()):
            break
except KeyboardInterrupt:
    print("SIGTERM detected... Stopping operations")
    print("This is not a good idea. I am unable to save any work, dataloss imminent!")
# END UI STUFF        


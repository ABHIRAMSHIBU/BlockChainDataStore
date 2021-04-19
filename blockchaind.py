#!/usr/bin/env python
import datetime
import hashlib
import os
import pickle
import base64
import rsa
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

sender_private = b'MIICYAIBAAKBgQDCmg8eXbWUMfTJLrEGtu4ZnmpZEdtAgzLyoapbdnfIEARHye9ZETScrCX4sT0FJGcjrKiHQtSobau7NPIgDWw9kU3UpUekNRVSf0roOAQg84slJoRBI1f34l9NBjgms1gkCB6FqsnVD3OgTcErMaUL8hDsXPYsnKNnhZP5IrHh+wIDAQABAoGAenbvSsHYUoG5tZ3fpAUdBBxQeusk2o12U4Dvr413RfzmZLMtIBUW0f34C3CmoQTOr4GpsS2anMAf0bk4mGZOcMyuY8cEl2O5oUfm03LOxGoR2bw3/v/g0aPWIxJFulD6aCvAYhuUSngAZyLVJSIu3hsUqBB/Oye9YVyVxk/LEekCRQDbZwE/cP6stykxYfLbuGDsxwzbK8VUSbniJPAJmpHj3Lsh5RgddfQ+KXgRuiy4WTM3Wa2e5/VgVaxKR4W/7O+m7U6tJQI9AOMQAwD20fygTfNC6342OWVnoO8mSH+8TC/3WbgumxmW2dYpFAwWLAgtUDEs1VrVdSpEaUkfWa6pro94nwJEAWSF/YEaHL6M5GNax0pEUzxwOHPurLpLE8RoQadZhbjA91Yc8RLumfZpbLNh1Um7qX5IO9n9FL92eII7txwp6UVYWoECPGW5ua7H5WHJq8KNO5XK00IEAEzEGPzpLjTbGx3x+1imhad1td6IXGe5bVDqphdQxHIQPh8dZX9j06nBPwJFAKbIwDdJS3Zc/i/Gz3u8cDcX+a/HP6XVcmBfIQmJnqnfh+CX67nDI9s51kGzB8Qhw2TQtW8ifCKCUFXEhd/IoqYVVu6L'
sender_public = b'MIGJAoGBAMKaDx5dtZQx9MkusQa27hmealkR20CDMvKhqlt2d8gQBEfJ71kRNJysJfixPQUkZyOsqIdC1Khtq7s08iANbD2RTdSlR6Q1FVJ/Sug4BCDziyUmhEEjV/fiX00GOCazWCQIHoWqydUPc6BNwSsxpQvyEOxc9iyco2eFk/kiseH7AgMBAAE='
reciever_public = b'MIGJAoGBAMzzGN/1Ohd2g8t7EiRj5PARxVVhMrEH9WPz82Up2lxiNMN12LUXt+YaQ1kE2jRmCZi9gClmf1v1+p6pvKZAWRSVSTDzcpavfVwP+VqhED22JrwyMqOZbMBHLwIeaBWSdajhpcXTxMnWdPnCywGAKW2JBggEDpT3OK9yOEWq4XnJAgMBAAE='
reciever_private = b'MIICXwIBAAKBgQDM8xjf9ToXdoPLexIkY+TwEcVVYTKxB/Vj8/NlKdpcYjTDddi1F7fmGkNZBNo0ZgmYvYApZn9b9fqeqbymQFkUlUkw83KWr31cD/laoRA9tia8MjKjmWzARy8CHmgVknWo4aXF08TJ1nT5wssBgCltiQYIBA6U9zivcjhFquF5yQIDAQABAoGAOBMPLD+BLGg9uQ+sMA6w1cpW7nxQjUU7K6TUZEpmNz6bZxs4NpwNscRfxtxgA1QjrgmzJiCoGfYcIwsXnLbJF+5ybPk13Qu3MvAzyljLlhtmxKUy2VyUu4nncfHIpCeHiCrRcJ2uzbpnc0hlL34ZCTe3vbejPPud21Z+h3liQwECRQDPcu8XpR0rWxG3YdfO96ov9Q6RXqnHdt35PSLy9yCoUDqAklw3h+FaR3FCe4S4lQCSiNLxecSPdOnH6/DGHhuQHp2yoQI9APzqarJgdaCUjkEbaqZJfpbqs1kIpyVLyDsA1O4sdZlBM3I/MlFp6chvsLPEBNkzPTkmqZ1UwfJV7BEeKQJEK2J0ElPbt9eB6wIxaf1twD3V4B0WELsRTTC2AG4ijFDLC1yQoKRwQrsyOp8ucJPo3Lx0sT+wFfhzc/YqEqT1Sry8akECPGv2hWVv18aco70XPweNCATUW4r+Lpu1JdxKFps1T14Efzmd0JUAaVOumfejDY7KWLA02OLYc5JHK2aDQQJEeuddtBwpCQshahPI9RdwLTDnfcF9ysp2f5KqcuvIwOVL6mOT/WmRNH2DAL3/LaoHYuYSugTMNRNaL2edqJ1V+dj9rcc='

block=create_block(header=create_block_header(id=0,version=0,previous_block_hash=0,
                   merkle_root_hash=0,timestamp=str(datetime.datetime.now()),difficulty=0,
                   nonce=0),transaction=[create_transaction(sender_pub=sender_public,
                   sender_priv=sender_private,reciever=1,metadata=b"some metadata",
                   data=b"some data")],transaction_counter=1)
saveBlock(block)
if(loadBlockAndVerify(0)==block):
    print("Verified!")
print(check_transaction(sender_public, block["TRANSACTION"][0]))


        


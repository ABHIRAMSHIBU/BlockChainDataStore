#!/usr/bin/env python
import datetime
import hashlib
import os
import pickle
import base64
# Time stuff - Just for redability these are defined.. completely useless use for functions
def strtotimestamp(date):
    return datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f")
# END Time stuff

# Block chain skelliton code
def create_transaction(sender,reciever,metadata,data):
    transaction={"SENDER":sender,"RECIEVER":reciever,"TIMESTAMP":str(datetime.datetime.now()),"METADATA":metadata,"DATA":data}
    return transaction
def create_block(header,transaction: list,transaction_counter):
    block={"HEADER":header,"TRANSATION":transaction,"TRANSACTION_COUNTER":transaction_counter}
    return block
def create_block_header(id,version,previous_block_hash,merkle_root_hash,timestamp,difficulty,nonce):
    block_header={"ID":id,"VERSION":version,"PREVIOUS_BLOCK_HASH":previous_block_hash,"MERKLE_ROOT_HASH":merkle_root_hash,"TIMESTAMP":timestamp,"DIFFICULTY":difficulty,"NONCE":nonce}
    return block_header
# END Block chain skelliton

def saveBlock(block,N=False): # N means dont do anything just show what it might do.
    stats={"current":-1,"hash":0,"block_count":0}
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
        stats={"current":nextcurrent,"hash":nexthash,"block_count":nextcount}
        if(nextcurrent==0):
            stats["block_count"]=1 # Genesis block
        f.write(pickle.dumps(stats))
        f.close()
        f=open("blockchain/block_"+str(nextcurrent),"wb")
        f.write(pickle.dumps([block,nexthash]))
block=create_block(create_block_header(0,0,0,0,str(datetime.datetime.now()),0,0),[create_transaction(0,1,b"some metadata",b"some data")],1)
saveBlock(block)
    


        


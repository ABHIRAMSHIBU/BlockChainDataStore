#!/usr/bin/env python
import datetime
def create_transaction(sender,reciever,metadata,data):
    transaction={"SENDER":sender,"RECIEVER":reciever,"TIMESTAMP":datetime.datetime.now(),"METADATA":metadata,"DATA":data}
    return transaction
def create_block(header,transaction: list,transaction_counter):
    block={"HEADER":header,"TRANSATION":transaction,"TRANSACTION_COUNTER":transaction_counter}
    return block
def create_block_header(version,previous_block_hash,merkle_root_hash,timestamp,difficulty,nonce):
    block_header={"VERSION":version,"PREVIOUS_BLOCK_HASH":previous_block_hash,"MERKLE_ROOT_HASH":merkle_root_hash,"TIMESTAMP":timestamp,"DIFFICULTY":difficulty,"NONCE":nonce}
    return block_header
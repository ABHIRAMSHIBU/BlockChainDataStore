#!/usr/bin/env python3
import rsa
import base64

key = rsa.newkeys(1024)
public_key=base64.standard_b64encode(key[0].save_pkcs1("DER"))
private_key=base64.standard_b64encode(key[1].save_pkcs1("DER"))
print("Public Key")
print(public_key)
print()
print()
print("Private Key")
print(private_key)
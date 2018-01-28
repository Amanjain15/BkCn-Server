# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from general.methods import JWT
from transaction import Transaction
import ecdsa, hashlib, socket, json, ast
from login.models import user_data, auth_user
@JWT
def create_transaction_POST(request, user, response):
	reciever_mobile = request.POST.get('reciever')
	reciever = user_data.objects.get(mobile = reciever_mobile)

	sender_public_key = auth_user.objects.get(user = user).public_key
	reciever_public_key = auth_user.objects.get(user = reciever).public_key
	product_hash = request.POST.get('product_id')

	txn = Transaction(sender_public_key, reciever_public_key, product_hash)

	if txn.authenticated:
		txn.broadcast()
	else:
		response['success'] = False
		response['message'] = "Transaction Authentication Failed"

	return JsonResponse(response)

def product_owners_POST(request):
	response = {
	'success':True,
	'message':'msg'
	}

	state = cal_state()

	product_hash = request.GET.get('product_hash')
	product_hash = request.GET.get('product_hash')

	response['owner'] = state[product_hash][-1]
	response['owner'] = auth_user.objects.get(public_key = response['owner']).user.mobile
	response['manufacturer'] = state[product_hash][0]
	response['manufacturer'] = auth_user.objects.get(public_key = response['manufacturer']).user.mobile
	return JsonResponse(response)

def cal_state():
	blocks = get_blocks()
	state = {}
	for block in blocks:
		if block != '':
			block = json.loads(block)
			for txn in block['txns']:
				print"txn,",txn
				try:
					state[txn['product_hash']][0]
				except:
					state[txn['product_hash']] = []
				print "h1"
				state[txn['product_hash']].append(txn['reciever_public_key'])
				print "h2"
	print "state found"
	return state

def get_blocks():
	data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	data_socket.connect(('127.0.0.1', 8003))
	data = ''
	while 1:
		buff = data_socket.recv(1024)
		data = data + buff
		if not buff: break
	data = json.loads(data)
	# print data
	return data['blocks']


def genPublicKey(senderSecretKey):
    sk = ecdsa.SigningKey.from_string(senderSecretKey.decode('hex'), curve=ecdsa.SECP256k1)
    return sk.verifying_key.to_string().encode('hex')

def genHash(senderSecretKey ,senderPubKey, recieverPubKey, product):
	toBeHashed = senderPubKey + recieverPubKey + product
	sk = ecdsa.SigningKey.from_string(senderSecretKey.decode('hex'), curve=ecdsa.SECP256k1)
	sign = sk.sign(toBeHashed)
	return sign.encode('hex')

# print "aaaaaaaaaaaaaaaaaaaaaaaa"

def ghash(data):
	return hashlib.sha256(data).digest().encode('hex')

a = ghash("a")
b = ghash("b")
c = ghash("c")
d = ghash("d")

A1 = ghash("a1")
B1 = ghash("b1")
C1 = ghash("c1")

AP1 = genPublicKey(A1)
BP1 = genPublicKey(B1)
CP1 = genPublicKey(C1)

transactions = [
	{
	"sender_public_key":AP1,
	"reciever_public_key":AP1,
	"product_hash":a,
	"hashed":genHash(A1,AP1,AP1,a)
	},{
	"sender_public_key":BP1,
	"reciever_public_key":BP1,
	"product_hash":b,
	"hashed":genHash(B1,BP1,BP1,b)
	},{
	"sender_public_key":CP1,
	"reciever_public_key":CP1,
	"product_hash":c,
	"hashed":genHash(C1,CP1,CP1,c)
	},{
	"sender_public_key":CP1,
	"reciever_public_key":CP1,
	"product_hash":d,
	"hashed":genHash(C1,CP1,CP1,d)
	},{
	"sender_public_key":AP1,
	"reciever_public_key":BP1,
	"product_hash":a,
	"hashed":genHash(A1,AP1,BP1,a)
	},{
	"sender_public_key":CP1,
	"reciever_public_key":BP1,
	"product_hash":c,
	"hashed":genHash(C1,CP1,BP1,c)
	},{
	"sender_public_key":BP1,
	"reciever_public_key":AP1,
	"product_hash":a,
	"hashed":genHash(B1,BP1,AP1,a)
	},{
	"sender_public_key":BP1,
	"reciever_public_key":AP1,
	"product_hash":b,
	"hashed":genHash(B1,BP1,AP1,b)
	}
]

def runt_GET(request):
	get_blocks()
	# for txn in transactions:
	# 	print txn
	# 	txn = Transaction(txn['sender_public_key'], txn['reciever_public_key'], txn['product_hash'], txn['hashed'])
	# 	if txn.authenticated:
	# 		txn.broadcast()
	# 	else:
	# 		response['success'] = False
	# 		response['message'] = "Transaction Authentication Failed"
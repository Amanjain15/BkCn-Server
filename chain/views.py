# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from general.methods import JWT
from transaction import Transaction
import ecdsa

@JWT
def create_transaction_POST(request, response):
	sender_public_key = request.POST.get('sender_public_key')
	reciever_public_key = request.POST.get('reciever_public_key')
	product_hash = request.POST.get('product_hash')
	hashed = request.POST.get('hashed')

	txn = Transaction(sender_public_key, reciever_public_key, product_hash, hashed)

	if txn.authenticated:
		txn.broadcast()
	else:
		response['success'] = False
		response['message'] = "Transaction Authentication Failed"

	return JsonResponse(response)
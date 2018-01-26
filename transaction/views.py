from django.shortcuts import render
from .models import txnBufferData
# Create your views here.
import datetime
import hashlib, json, sys

def hashMe(msg=""):
	# For convenience, this is a helper function that wraps our hashing algorithm
	if type(msg)!=str:
		msg = json.dumps(msg,sort_keys=True)  # If we don't sort keys, we can't guarantee repeatability!
		
	if sys.version_info.major == 2:
		return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')
	else:
		return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

def txn(request):
	response_json={}
	txn_json={}
	if request.method == 'POST':
		try:
			sender=request.POST.get('sender')
			receiver=request.POST.get('receiver')
			product_hash=request.POST.get('product_hash')
			txn_hash=hashME(sender+receiver+product_hash+str(datetime.now()))
			# txn,created=txnBufferData.objects.get_or_create(sender=sender,receiver=receiver,product_hash=product_hash,txn_hash=txn_hash)
			# set_attr(txn,'status',1);
			print 'txn sent to peers'
			broadcast_to_peers(str(sender+receiver+product_hash+txn_hash))
			response_json['success']=True
			response_json['message']='Your Transaction has been queued.'
		except Exception e:
			print str(e)
			response_json['message']='error'
			response_json['success']=False
		return JsonRespnse(response_json)

# genesisBlockTxns = []
# genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}
# genesisHash = hashMe( genesisBlockContents )
# genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
# genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)

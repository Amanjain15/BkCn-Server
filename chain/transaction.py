import json, ecdsa, socket
BROADCASTING_PORT = 8001
newTransactionMsg = "new Transaction"

class Transaction:
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def __init__(self, sender_public_key, reciever_public_key, product_hash, hashed):
		self.sender_public_key = sender_public_key
		self.reciever_public_key = reciever_public_key
		self.product_hash = product_hash
		self.hashed = hashed
		self.authenticated = self.authenticate()
		self.message = newTransactionMsg

	def authenticate(self):
		vk = ecdsa.VerifyingKey.from_string(self.sender_public_key.decode('hex'), curve=ecdsa.SECP256k1)
		return vk.verify(self.hashed.decode('hex'), self.sender_public_key + self.reciever_public_key + self.product_hash)

	def broadcast(self):
		broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		broadcast_socket.bind(('', 0))
		broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		broadcast_socket.sendto(self.toJSON(), ('<broadcast>', BROADCASTING_PORT))

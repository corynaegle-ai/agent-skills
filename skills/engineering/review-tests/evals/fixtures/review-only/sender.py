PAYLOAD_VERSION = 1


class Sender:
    def __init__(self, transport):
        self.transport = transport
        self.receipts = {}

    def send(self, key, text):
        if key in self.receipts:
            return self.receipts[key]
        receipt = self.transport.send({"version": PAYLOAD_VERSION, "key": key, "text": text})
        self.receipts[key] = receipt
        return receipt

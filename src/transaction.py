from typing import List, Dict

class Transaction:
    def __init__(self, tx_id: str, inputs: List[Dict], outputs: List[Dict]):
        self.tx_id = tx_id
        self.inputs = inputs
        self.outputs = outputs
        self.fee = 0.0

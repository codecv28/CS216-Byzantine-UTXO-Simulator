class UTXOManager:
    def __init__(self):
        self.utxo_set = {}
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis_tx_id = "genesis"
        self.add_utxo(genesis_tx_id, 0, 50.0, "Alice")
        self.add_utxo(genesis_tx_id, 1, 30.0, "Bob")
        self.add_utxo(genesis_tx_id, 2, 20.0, "Charlie")
        self.add_utxo(genesis_tx_id, 3, 10.0, "David")
        self.add_utxo(genesis_tx_id, 4, 5.0, "Eve")
    
    def add_utxo(self, tx_id: str, index: int, amount: float, owner: str):
        key = (tx_id, index)
        self.utxo_set[key] = {
            "amount": amount,
            "owner": owner
        }
    
    def remove_utxo(self, tx_id: str, index: int):
        key = (tx_id, index)
        if key in self.utxo_set:
            self.utxo_set.pop(key)
        
    def get_amount(self, tx_id: str, index: int) -> float:
        key = (tx_id, index)
        if key not in self.utxo_set:
            raise ValueError(f"UTXO {key} not found")
        return self.utxo_set[key]["amount"]

    def get_balance(self, owner: str) -> float:
        balance = 0.0
        for utxo_data in self.utxo_set.values():
            if utxo_data["owner"] == owner:
                balance += utxo_data["amount"]
        return balance
    
    def exists(self, tx_id: str, index: int) -> bool:
        key = (tx_id, index)
        return key in self.utxo_set
    
    def get_utxos_for_owner(self, owner: str) -> list:
        utxos = []
        for key, utxo_data in self.utxo_set.items():
            tx_id, index = key
            if utxo_data["owner"] == owner:
                utxos.append({
                    "tx_id": tx_id,
                    "index": index,
                    "amount": utxo_data["amount"]
                })
        return utxos
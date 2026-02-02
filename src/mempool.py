# mempool.py
from typing import List, Tuple
from transaction import Transaction
from validator import validate_transaction
from utxo_manager import UTXOManager


class Mempool:
    def __init__(self, max_size: int = 50):
        self.transactions: List[Transaction] = []
        self.spent_utxos = set()   # (tx_id, index)
        self.max_size = max_size

#add transaction function

    def add_transaction(self, tx: Transaction, utxo_manager: UTXOManager) -> Tuple[bool, str]:
        # Validate transaction first
        is_valid, msg = validate_transaction(tx, utxo_manager, self)
        if not is_valid:
            return False, msg

        if len(self.transactions) >= self.max_size:
            removed = self.transactions.pop(0)
            for inp in removed.inputs:
                self.spent_utxos.discard((inp["prev_tx"], inp["index"]))

        # track spent UTXOs
        for inp in tx.inputs:
            self.spent_utxos.add((inp["prev_tx"], inp["index"]))

        self.transactions.append(tx)
        return True, "Transaction added to mempool"

#remove transaction function

    def remove_transaction(self, tx_id: str):
        remaining = []
        for tx in self.transactions:
            if tx.tx_id == tx_id:
                for inp in tx.inputs:
                    self.spent_utxos.discard((inp["prev_tx"], inp["index"]))
            else:
                remaining.append(tx)

        self.transactions = remaining
#get top transactions function
    def get_top_transactions(self, n: int) -> List[Transaction]:
        # sorting according to fees, high to low
        def fee(tx: Transaction):
            return tx.fee

        return sorted(self.transactions, key=fee, reverse=True)[:n]

    def clear(self):
        self.transactions.clear()
        self.spent_utxos.clear()

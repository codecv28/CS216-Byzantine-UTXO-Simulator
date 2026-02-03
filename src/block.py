from mempool import Mempool
from utxo_manager import UTXOManager
from transaction import Transaction
import time

def mine_block(miner_address: str, mempool: Mempool,
               utxo_manager: UTXOManager, num_txs: int = 5):

    selected_txs = mempool.get_top_transactions(num_txs)
    if not selected_txs:
        return

    total_fees = 0.0

    for tx in selected_txs:
        for inp in tx.inputs:
            utxo_manager.remove_utxo(inp["prev_tx"], inp["index"])

        for idx, out in enumerate(tx.outputs):
            utxo_manager.add_utxo(
                tx.tx_id,
                idx,
                out["amount"],
                out["address"]
            )

        total_fees += tx.fee
        mempool.remove_transaction(tx.tx_id)

    # Create coinbase transaction for miner reward (fees only, no block reward in this simulation)
    if total_fees > 0:
        coinbase_id = f"coinbase_{miner_address}_{int(time.time())}"
        utxo_manager.add_utxo(
            coinbase_id,
            0,
            total_fees,
            miner_address
        )

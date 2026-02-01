from mempool import Mempool
from utxo_manager import UTXOManager
from transaction import Transaction

def mine_block(miner_address: str, mempool: Mempool,
               utxo_manager: UTXOManager, num_txs: int = 5):

    print("Mining block")

    selected_txs = mempool.get_top_transactions(num_txs)
    if not selected_txs:
        print("No transactions to mine")
        return

    total_fees = 0.0

    for tx in selected_txs:
        # remove spent UTXOs
        for inp in tx.inputs:
            utxo_manager.remove_utxo(inp["prev_tx"], inp["index"])

        # add new UTXOs from outputs
        for idx, out in enumerate(tx.outputs):
            utxo_manager.add_utxo(
                tx.tx_id,
                idx,
                out["amount"],
                out["address"]
            )

        total_fees += tx.fee
        mempool.remove_transaction(tx.tx_id)

    # miner reward = total fees
    if total_fees > 0:
        utxo_manager.add_utxo(
            "coinbase",
            0,
            total_fees,
            miner_address
        )

    print(f"Block mined successfully!")
    print(f"Miner {miner_address} earned {total_fees} BTC")

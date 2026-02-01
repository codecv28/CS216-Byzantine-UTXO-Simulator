from typing import Tuple
from transaction import Transaction
from utxo_manager import UTXOManager
from mempool import Mempool


def validate_transaction(transaction: Transaction, utxo_manager: UTXOManager, mempool: Mempool) -> Tuple[bool, str]:

    inputs = transaction.inputs
    outputs = transaction.outputs

    # rule 1: All inputs must exist in UTXO set
    for input in inputs:
        if not utxo_manager.exists(input["prev_tx"], input["index"]):
            return False, f"UTXO {input['prev_tx']}:{input['index']} does not exist"

    #rule 2: No double-spending inside same transaction
    seen_inputs = set()
    for input in inputs:
        key = (input["prev_tx"], input["index"])
        if key in seen_inputs:
            return False, "Double spending detected within transaction"
        seen_inputs.add(key)

    #rule 5: No conflict with mempool (UTXO already spent by unconfirmed tx)
    for key in seen_inputs:
        if key in mempool.spent_utxos:
            return False, f"UTXO {key} already spent in mempool"

    #rule 4: No negative output amounts
    for output in outputs:
        if output["amount"] < 0:
            return False, "Negative output amount detected"

    #rule 3: Sum(inputs) >= Sum(outputs)
    input_amt = 0.0
    for input in inputs:
        amount = utxo_manager.get_amount(input["prev_tx"], input["index"])
        input_amt += amount

    output_amt = sum(output["amount"] for output in outputs)

    if input_amt < output_amt:
        return False, "Insufficient input amount"
    
    transaction.fee = input_amt - output_amt

    return True, "Transaction is valid"
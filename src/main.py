import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utxo_manager import UTXOManager
from mempool import Mempool
from transaction import Transaction
from block import mine_block
from test_scripts.test_scenarios import (
    run_all_tests, 
    test_1_basic_valid_transaction,
    test_2_multiple_inputs,
    test_3_double_spend_same_transaction,
    test_4_mempool_double_spend,
    test_5_insufficient_funds,
    test_6_negative_amount,
    test_7_zero_fee_transaction,
    test_8_race_attack_simulation,
    test_9_complete_mining_flow,
    test_10_unconfirmed_chain
)


def main():
    utxo = UTXOManager()
    mempool = Mempool()

    
    while True:
        print("\n=== Bitcoin Transaction Simulator ===")
        print("Initial UTXOs ( Genesis Block ) :")
        if not utxo.utxo_set:
                print("No UTXOs available")
        else:
            for k, v in utxo.utxo_set.items():
                print(f"{k} -> {v}")
        print("Main Menu :")
        print("1. Create new transaction")
        print("2. View UTXO set")
        print("3. View mempool")
        print("4. Mine block")
        print("5. Run test scenarios")
        print("6. Exit")

        ch = input("Enter choice: ").strip()

        if ch == "1":
            create_transaction(utxo, mempool)

        elif ch == "2":
            print(f"\n=== UTXO Set ===")
            if not utxo.utxo_set:
                print("No UTXOs available")
            else:
                for k, v in utxo.utxo_set.items():
                    print(f"{k} -> {v}")

        elif ch == "3":
            print(f"\n=== Mempool ===")
            if not mempool.transactions:
                print("Mempool is empty")
            else:
                print(f"Transactions in mempool: {len(mempool.transactions)}")
                print("-" * 60)
                for i, tx in enumerate(mempool.transactions):
                    print(f"Transaction {i+1}: {tx.tx_id}")
                    print(f"  Size: {tx.size_bytes} bytes")
                    print(f"  Fee: {tx.fee:.8f} BTC ({tx.fee_rate:.1f} sat/byte)")
                    print(f"  Inputs: {len(tx.inputs)}, Outputs: {len(tx.outputs)}")
                    print("-" * 60)

        elif ch == "4":
            miner_name = input("Enter miner name: ").strip()
            if not miner_name:
                print("Invalid miner name")
                continue
            print("Mining block...")
            
            if not mempool.transactions:
                print("No transactions to mine")
                continue
                
            selected_count = min(len(mempool.transactions), 5)
            selected_txs = mempool.get_top_transactions(selected_count)
            
            print(f"Selected {selected_count} highest fee transactions:")
            total_fees = 0
            for i, tx in enumerate(selected_txs):
                print(f"  {i+1}. {tx.tx_id} - Fee: {tx.fee:.8f} BTC ({tx.fee_rate:.1f} sat/byte)")
                total_fees += tx.fee
            
            print(f"Total fees collected: {total_fees:.8f} BTC")
            print(f"Miner {miner_name} receives {total_fees:.8f} BTC")
            
            mine_block(miner_name, mempool, utxo)
            print("Block mined successfully!")
            print(f"Removed {selected_count} transactions from mempool.")

        elif ch == "5":
            print("\nSelect test scenario:")
            print("1. Test 1: Basic Valid Transaction")
            print("2. Test 2: Multiple Inputs")
            print("3. Test 3: Double-Spend in Same Transaction")
            print("4. Test 4: Mempool Double-Spend")
            print("5. Test 5: Insufficient Funds")
            print("6. Test 6: Negative Amount")
            print("7. Test 7: Zero Fee Transaction")
            print("8. Test 8: Race Attack Simulation")
            print("9. Test 9: Complete Mining Flow")
            print("10. Test 10: Unconfirmed Chain")
            print("11. Run ALL tests")
            
            test_choice = input("Enter choice (1-11): ").strip()
            
            test_functions = {
                "1": test_1_basic_valid_transaction,
                "2": test_2_multiple_inputs,
                "3": test_3_double_spend_same_transaction,
                "4": test_4_mempool_double_spend,
                "5": test_5_insufficient_funds,
                "6": test_6_negative_amount,
                "7": test_7_zero_fee_transaction,
                "8": test_8_race_attack_simulation,
                "9": test_9_complete_mining_flow,
                "10": test_10_unconfirmed_chain,
                "11": run_all_tests
            }
            
            if test_choice in test_functions:
                test_functions[test_choice]()
            else:
                print("Invalid test choice")

        elif ch == "6":
            break

        else:
            print("Invalid choice")


def create_transaction(utxo, mempool):
    sender = input("Enter sender: ").strip()
    if not sender:
        print("Invalid sender")
        return
    
    balance = utxo.get_balance(sender)
    print(f"Available balance: {balance} BTC")
    
    if balance == 0:
        print(f"No balance for {sender}")
        return
    
    recipient = input("Enter recipient: ").strip()
    if not recipient:
        print("Invalid recipient")
        return
    
    try:
        amount = float(input("Enter amount: ").strip())
        if amount <= 0:
            print("Amount must be positive")
            return
        if amount > balance:
            print(f"Insufficient balance")
            return
    except ValueError:
        print("Invalid amount")
        return
    
    print("Creating transaction...")
    
    # Select UTXOs
    sender_utxos = utxo.get_utxos_for_owner(sender)
    selected_utxos = []
    total_selected = 0
    
    for utxo_info in sender_utxos:
        if total_selected >= amount:
            break
        selected_utxos.append(utxo_info)
        total_selected += utxo_info["amount"]
    
    inputs = []
    for utxo_info in selected_utxos:
        inputs.append({
            "prev_tx": utxo_info["tx_id"],
            "index": utxo_info["index"],
            "owner": sender
        })
    
    outputs = [{"amount": amount, "address": recipient}]
    
    # Create preliminary transaction to calculate size
    import time
    tx_id = f"tx_{sender.lower()}_{recipient.lower()}_{int(time.time())}"
    temp_tx = Transaction(tx_id, inputs, outputs)
    
    print(f"\nTransaction size: {temp_tx.size_bytes} bytes")
    
    # Show fee rate options (realistic Bitcoin fee rates)
    print("\nFee Rate Options:")
    print("1. Low Priority (1 sat/byte) - May take hours")
    print("2. Medium Priority (10 sat/byte) - ~30 minutes") 
    print("3. High Priority (50 sat/byte) - ~10 minutes")
    print("4. Custom fee rate")
    
    fee_choice = input("Select fee option (1-4): ").strip()
    
    fee_rates = {
        "1": 1.0,    # Low priority
        "2": 10.0,   # Medium priority  
        "3": 50.0,   # High priority
    }
    
    if fee_choice in fee_rates:
        fee_rate = fee_rates[fee_choice]
    elif fee_choice == "4":
        try:
            fee_rate = float(input("Enter custom fee rate (sat/byte): ").strip())
            if fee_rate < 0:
                print("Fee rate must be positive")
                return
        except ValueError:
            print("Invalid fee rate")
            return
    else:
        print("Invalid choice, using medium priority (10 sat/byte)")
        fee_rate = 10.0
    
    # Calculate fee
    temp_tx.set_fee_rate(fee_rate)
    required_fee = temp_tx.fee
    
    print(f"Fee rate: {fee_rate} sat/byte")
    print(f"Required fee: {required_fee:.8f} BTC")
    
    # Check if we have enough for amount + fee
    if total_selected < amount + required_fee:
        print(f"Insufficient balance for amount + fee. Need {amount + required_fee:.8f} BTC, have {total_selected:.8f} BTC")
        return
    
    # Calculate change after fee
    change = total_selected - amount - required_fee
    if change > 0:
        outputs.append({"amount": change, "address": sender})
        print(f"Change: {change:.8f} BTC")
    
    # Create final transaction
    tx = Transaction(tx_id, inputs, outputs)
    tx.set_fee_rate(fee_rate)
    
    success, message = mempool.add_transaction(tx, utxo)
    
    if success:
        print(f"\n✅ Transaction created successfully!")
        print(f"Transaction ID: {tx_id}")
        print(f"Fee paid: {tx.fee:.8f} BTC ({fee_rate} sat/byte)")
        print(f"Transaction added to mempool.")
        print(f"Mempool now has {len(mempool.transactions)} transactions.")
    else:
        print(f"❌ Transaction failed: {message}")


if __name__ == "__main__":
    main()
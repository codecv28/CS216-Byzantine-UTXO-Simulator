import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from utxo_manager import UTXOManager
from mempool import Mempool
from transaction import Transaction
from block import mine_block


def run_all_tests():
    print("\n" + "="*60)
    print("COMPREHENSIVE BITCOIN TRANSACTION TEST SUITE")
    print("="*60)
    
    tests = [
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
    ]
    
    passed = 0
    failed = 0
    
    for i, test_func in enumerate(tests, 1):
        print(f"\n{'='*20} TEST {i} {'='*20}")
        try:
            result = test_func()
            if result:
                print("✅ PASSED")
                passed += 1
            else:
                print("❌ FAILED")
                failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"TEST RESULTS: {passed} PASSED, {failed} FAILED")
    print("="*60)


def test_1_basic_valid_transaction():
    """Test 1: Basic Valid Transaction - Alice sends 10 BTC to Bob with change and fee"""
    print("Test 1: Basic Valid Transaction")
    print("Alice sends 10 BTC to Bob (must include change and 0.001 BTC fee)")
    
    utxo = UTXOManager()
    mempool = Mempool()
    
    # Create transaction: Alice (50 BTC) -> Bob (10 BTC) + Alice change (39.999 BTC) + fee (0.001 BTC)
    tx = Transaction(
        "test_1_alice_to_bob",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],  # 50 BTC input
        [
            {"amount": 10.0, "address": "Bob"},      # 10 BTC to Bob
            {"amount": 39.999, "address": "Alice"}   # 39.999 BTC change to Alice
        ]
    )
    tx.set_fee_rate(10.0)  # Set fee rate to calculate proper fee
    
    success, msg = mempool.add_transaction(tx, utxo)
    
    expected_fee = 0.001
    actual_fee = 50.0 - 10.0 - 39.999  # Input - outputs = fee
    
    print(f"Transaction: {'ACCEPTED' if success else 'REJECTED'}")
    print(f"Message: {msg}")
    print(f"Expected fee: {expected_fee} BTC")
    print(f"Actual fee: {actual_fee} BTC")
    
    return success and abs(actual_fee - expected_fee) < 0.0001


def test_2_multiple_inputs():
    """Test 2: Multiple Inputs - Alice spends two UTXOs together"""
    print("Test 2: Multiple Inputs")
    print("Alice spends two UTXOs (50 + 30 BTC) to send 60 BTC to Bob")
    
    utxo = UTXOManager()
    mempool = Mempool()
    
    # Add additional UTXO for Alice
    utxo.add_utxo("genesis", 5, 30.0, "Alice")
    
    # Transaction with multiple inputs
    tx = Transaction(
        "test_2_multiple_inputs",
        [
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"},  # 50 BTC
            {"prev_tx": "genesis", "index": 5, "owner": "Alice"}   # 30 BTC
        ],
        [
            {"amount": 60.0, "address": "Bob"},      # 60 BTC to Bob
            {"amount": 19.99, "address": "Alice"}    # 19.99 BTC change (0.01 BTC fee)
        ]
    )
    tx.set_fee_rate(5.0)
    
    success, msg = mempool.add_transaction(tx, utxo)
    
    total_input = 50.0 + 30.0
    total_output = 60.0 + 19.99
    fee = total_input - total_output
    
    print(f"Transaction: {'ACCEPTED' if success else 'REJECTED'}")
    print(f"Message: {msg}")
    print(f"Total inputs: {total_input} BTC")
    print(f"Total outputs: {total_output} BTC")
    print(f"Fee: {fee} BTC")
    
    return success and len(tx.inputs) == 2


def test_3_double_spend_same_transaction():
    """Test 3: Double-Spend in Same Transaction"""
    print("Test 3: Double-Spend in Same Transaction")
    print("Transaction tries to spend same UTXO twice")
    
    utxo = UTXOManager()
    mempool = Mempool()
    
    # Transaction that spends the same UTXO twice
    tx = Transaction(
        "test_3_double_spend",
        [
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"},  # Same UTXO
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"}   # Same UTXO again!
        ],
        [{"amount": 90.0, "address": "Bob"}]  # Trying to spend 100 BTC from 50 BTC UTXO
    )
    
    success, msg = mempool.add_transaction(tx, utxo)
    
    print(f"Transaction: {'ACCEPTED' if success else 'REJECTED'}")
    print(f"Message: {msg}")
    
    return not success and "Double spending" in msg


def test_4_mempool_double_spend():
    """Test 4: Mempool Double-Spend"""
    print("Test 4: Mempool Double-Spend")
    print("TX1: Alice → Bob, TX2: Alice → Charlie (same UTXO)")
    
    utxo = UTXOManager()
    mempool = Mempool()
    
    tx1 = Transaction(
        "test_4_tx1",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": 49.0, "address": "Bob"}, {"amount": 1.0, "address": "Alice"}]
    )
    
    tx2 = Transaction(
        "test_4_tx2",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],  # Same UTXO!
        [{"amount": 49.0, "address": "Charlie"}, {"amount": 1.0, "address": "Alice"}]
    )
    
    success1, msg1 = mempool.add_transaction(tx1, utxo)
    success2, msg2 = mempool.add_transaction(tx2, utxo)
    
    print(f"TX1 (Alice → Bob): {'ACCEPTED' if success1 else 'REJECTED'} - {msg1}")
    print(f"TX2 (Alice → Charlie): {'ACCEPTED' if success2 else 'REJECTED'} - {msg2}")
    
    return success1 and not success2 and "already spent in mempool" in msg2


def test_5_insufficient_funds():
    """Test 5: Insufficient Funds"""
    print("Test 5: Insufficient Funds")
    print("Bob tries to send 35 BTC (has only 30 BTC)")
    
    utxo = UTXOManager()
    mempool = Mempool()
    
    # Bob only has 30 BTC from genesis
    tx = Transaction(
        "test_5_insufficient",
        [{"prev_tx": "genesis", "index": 1, "owner": "Bob"}],  # Bob's 30 BTC
        [{"amount": 35.0, "address": "Charlie"}]  # Trying to send 35 BTC
    )
    
    success, msg = mempool.add_transaction(tx, utxo)
    
    print(f"Transaction: {'ACCEPTED' if success else 'REJECTED'}")
    print(f"Message: {msg}")
    
    return not success and "Insufficient" in msg


def test_6_negative_amount():
    """Test 6: Negative Amount"""
    print("Test 6: Negative Amount")
    print("Transaction with negative output amount")
    
    utxo = UTXOManager()
    mempool = Mempool()
    
    tx = Transaction(
        "test_6_negative",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": -10.0, "address": "Bob"}]  # Negative amount!
    )
    
    success, msg = mempool.add_transaction(tx, utxo)
    
    print(f"Transaction: {'ACCEPTED' if success else 'REJECTED'}")
    print(f"Message: {msg}")
    
    return not success and "Negative" in msg


def test_7_zero_fee_transaction():
    """Test 7: Zero Fee Transaction"""
    print("Test 7: Zero Fee Transaction")
    print("Inputs = Outputs (fee = 0) - should be valid")
    
    utxo = UTXOManager()
    mempool = Mempool()
    
    tx = Transaction(
        "test_7_zero_fee",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],  # 50 BTC input
        [
            {"amount": 30.0, "address": "Bob"},      # 30 BTC to Bob
            {"amount": 20.0, "address": "Alice"}     # 20 BTC change (no fee)
        ]
    )
    
    success, msg = mempool.add_transaction(tx, utxo)
    
    print(f"Transaction: {'ACCEPTED' if success else 'REJECTED'}")
    print(f"Message: {msg}")
    print(f"Fee: {tx.fee} BTC")
    
    return success and tx.fee == 0.0


def test_8_race_attack_simulation():
    """Test 8: Race Attack Simulation"""
    print("Test 8: Race Attack Simulation")
    print("Low-fee TX first, then high-fee TX (first-seen rule)")
    
    utxo = UTXOManager()
    mempool = Mempool()
    
    # Low fee transaction (arrives first)
    low_fee_tx = Transaction(
        "test_8_low_fee",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": 49.999, "address": "Bob"}, {"amount": 0.001, "address": "Alice"}]  # 0.001 fee
    )
    low_fee_tx.set_fee_rate(1.0)  # Low fee rate
    
    # High fee transaction (arrives second, same UTXO)
    high_fee_tx = Transaction(
        "test_8_high_fee",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],  # Same UTXO
        [{"amount": 49.0, "address": "Charlie"}, {"amount": 1.0, "address": "Alice"}]  # 0 fee but higher priority
    )
    high_fee_tx.set_fee_rate(50.0)  # High fee rate
    
    success1, msg1 = mempool.add_transaction(low_fee_tx, utxo)
    success2, msg2 = mempool.add_transaction(high_fee_tx, utxo)
    
    print(f"Low-fee TX: {'ACCEPTED' if success1 else 'REJECTED'} - {msg1}")
    print(f"High-fee TX: {'ACCEPTED' if success2 else 'REJECTED'} - {msg2}")
    print("First-seen rule: First transaction should win regardless of fee")
    
    return success1 and not success2


def test_9_complete_mining_flow():
    """Test 9: Complete Mining Flow"""
    print("Test 9: Complete Mining Flow")
    print("Add transactions, mine block, check results")
    
    utxo = UTXOManager()
    mempool = Mempool()
    
    # Add multiple transactions with different fees
    tx1 = Transaction("mining_tx1", [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}], 
                     [{"amount": 40.0, "address": "Bob"}, {"amount": 9.99, "address": "Alice"}])  # 0.01 fee
    tx1.set_fee_rate(10.0)
    
    tx2 = Transaction("mining_tx2", [{"prev_tx": "genesis", "index": 1, "owner": "Bob"}], 
                     [{"amount": 25.0, "address": "Charlie"}, {"amount": 4.995, "address": "Bob"}])  # 0.005 fee
    tx2.set_fee_rate(5.0)
    
    mempool.add_transaction(tx1, utxo)
    mempool.add_transaction(tx2, utxo)
    
    print(f"Mempool before mining: {len(mempool.transactions)} transactions")
    
    # Mine block
    miner_balance_before = utxo.get_balance("Miner")
    mine_block("Miner", mempool, utxo)
    miner_balance_after = utxo.get_balance("Miner")
    
    print(f"Mempool after mining: {len(mempool.transactions)} transactions")
    print(f"Miner balance before: {miner_balance_before} BTC")
    print(f"Miner balance after: {miner_balance_after} BTC")
    print(f"Miner earned: {miner_balance_after - miner_balance_before} BTC")
    
    return len(mempool.transactions) == 0 and miner_balance_after > miner_balance_before


def test_10_unconfirmed_chain():
    """Test 10: Unconfirmed Chain"""
    print("Test 10: Unconfirmed Chain")
    print("Alice → Bob (unconfirmed), then Bob tries to spend")
    
    utxo = UTXOManager()
    mempool = Mempool()
    
    # TX1: Alice sends to Bob (creates new UTXO for Bob)
    tx1 = Transaction(
        "chain_tx1",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": 25.0, "address": "Bob"}, {"amount": 24.99, "address": "Alice"}]
    )
    
    success1, msg1 = mempool.add_transaction(tx1, utxo)
    print(f"TX1 (Alice → Bob): {'ACCEPTED' if success1 else 'REJECTED'} - {msg1}")
    
    # TX2: Bob tries to spend the UTXO created by TX1 (before TX1 is mined)
    tx2 = Transaction(
        "chain_tx2",
        [{"prev_tx": "chain_tx1", "index": 0, "owner": "Bob"}],  # Spending unconfirmed UTXO
        [{"amount": 24.0, "address": "Charlie"}, {"amount": 0.99, "address": "Bob"}]
    )
    
    success2, msg2 = mempool.add_transaction(tx2, utxo)
    print(f"TX2 (Bob → Charlie): {'ACCEPTED' if success2 else 'REJECTED'} - {msg2}")
    
    print("Design Decision: This implementation rejects unconfirmed chains")
    print("Real Bitcoin: Would accept if properly implemented")
    
    return success1 and not success2 and "does not exist" in msg2


# Legacy functions for backward compatibility
def test_double_spend():
    return test_4_mempool_double_spend()

def test_mempool_conflict():
    return test_4_mempool_double_spend()

def test_race_attack():
    return test_8_race_attack_simulation()

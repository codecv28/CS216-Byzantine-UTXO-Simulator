import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from utxo_manager import UTXOManager
from mempool import Mempool
from transaction import Transaction


def run_all_tests():
    print("\n=== Running Test Scenarios ===\n")
    test_double_spend()
    test_mempool_conflict()
    test_race_attack()


def test_double_spend():
    print("Test 1: Double spend")

    utxo = UTXOManager()
    mempool = Mempool()

    utxo.add_utxo("genesis", 0, 50.0, "Alice")

    tx1 = Transaction(
        "tx1",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": 10, "address": "Bob"}]
    )

    tx2 = Transaction(
        "tx2",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": 10, "address": "Charlie"}]
    )

    ok, msg = mempool.add_transaction(tx1, utxo)
    print("TX1:", ok, msg)

    ok, msg = mempool.add_transaction(tx2, utxo)
    print("TX2:", ok, msg)

    print()


def test_mempool_conflict():
    print("Test 2: Mempool conflict")

    utxo = UTXOManager()
    mempool = Mempool()

    utxo.add_utxo("genesis", 0, 50.0, "Alice")

    tx1 = Transaction(
        "tx3",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": 5, "address": "Bob"}]
    )

    tx2 = Transaction(
        "tx4",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": 5, "address": "Charlie"}]
    )

    ok, msg = mempool.add_transaction(tx1, utxo)
    print("TX1:", ok, msg)

    ok, msg = mempool.add_transaction(tx2, utxo)
    print("TX2:", ok, msg)

    print()


def test_race_attack():
    print("Test 3: Race attack (first seen rule)")

    utxo = UTXOManager()
    mempool = Mempool()

    utxo.add_utxo("genesis", 0, 50.0, "Alice")

    low_fee_tx = Transaction(
        "tx_low",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": 49.999, "address": "Bob"}]
    )

    high_fee_tx = Transaction(
        "tx_high",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": 40, "address": "Charlie"}]
    )

    ok, msg = mempool.add_transaction(low_fee_tx, utxo)
    print("Low fee TX:", ok, msg)

    ok, msg = mempool.add_transaction(high_fee_tx, utxo)
    print("High fee TX:", ok, msg)

    print()

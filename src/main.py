import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utxo_manager import UTXOManager
from tests.test_scenarios import run_all_tests


def main():

    utxo = UTXOManager()

    utxo.add_utxo("genesis", 0, 50.0, "Alice")
    utxo.add_utxo("genesis", 1, 30.0, "Bob")
    utxo.add_utxo("genesis", 2, 20.0, "Charlie")
    utxo.add_utxo("genesis", 3, 10.0, "David")
    utxo.add_utxo("genesis", 4, 5.0, "Eve")

    while True:
        print("\n=== Bitcoin Transaction Simulator ===")
        print("1. Create new transaction")
        print("2. View UTXO set")
        print("3. View mempool")
        print("4. Mine block")
        print("5. Run test scenarios")
        print("6. Exit")

        ch = input("Enter choice: ").strip()

        if ch == "1":
            print("Create transaction (will be connected later).")

        elif ch == "2":
            for k, v in utxo.utxo_set.items():
                print(k, "->", v)

        elif ch == "3":
            print("Mempool not wired yet.")

        elif ch == "4":
            print("Mining not wired yet.")

        elif ch == "5":
            run_all_tests()

        elif ch == "6":
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

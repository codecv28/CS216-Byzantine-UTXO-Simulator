# Bitcoin Transaction Simulator

## Team: Byzantine

### Team Members
- **Mane Abhishek Ganesh** — 240001043
- **Chetan Verma** — 240001022
- **Dhoke Vinod Eknath** — 240001025
- **Sahil Hedaoo** — 240041032

---

##  Overview

This project implements a comprehensive Bitcoin transaction simulator that demonstrates core blockchain concepts including UTXO management, transaction validation, mempool operations, mining, and fee mechanisms. The simulator provides an interactive command-line interface for creating transactions, managing a mempool, and mining blocks.

##  Features

- **UTXO Management**: Complete Unspent Transaction Output tracking
- **Transaction Creation**: Interactive transaction builder with fee calculation
- **Mempool Operations**: Transaction pool with priority based ordering
- **Mining Simulation**: Block mining with fee collection
- **Fee System**: Realistic Bitcoin style fee calculation (sat/byte)
- **Validation Engine**: Comprehensive transaction validation rules
- **Double-Spend Prevention**: Mempool conflict detection
- **Race Attack Simulation**: First-seen rule implementation

##  Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/codecv28/CS216-Byzantine-UTXO-Simulator
   cd Blockchain
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```


##  How to Run

### Start the Simulator
```bash
python src/main.py
```

### Main Menu Options
1. **Create new transaction** - Interactive transaction builder
2. **View UTXO set** - Display all unspent transaction outputs
3. **View mempool** - Show pending transactions with fees
4. **Mine block** - Mine transactions from mempool
5. **Run test scenarios** - Execute comprehensive test suite
6. **Exit** - Close the simulator

### Creating Transactions
1. Select option 1 from main menu
2. Enter sender address (Alice, Bob, Charlie, David, Eve)
3. Enter recipient address
4. Enter amount to send
5. Choose fee priority:
   - Low Priority (1 sat/byte) 
   - Medium Priority (10 sat/byte) 
   - High Priority (50 sat/byte) 
   - Custom fee rate

### Running Tests
Select option 5 from main menu, then choose:
- Individual tests (1-10) for specific scenarios
- Option 11 to run all tests with comprehensive results

##  System Design

### Architecture Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Transaction   │    │     Mempool     │    │  UTXO Manager   │
│   - Inputs      │    │   - Validation  │    │   - Genesis     │
│   - Outputs     │    │   - Priority    │    │   - Balance     │
│   - Fee Calc    │    │   - Conflicts   │    │   - Tracking    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │    Validator    │
                    │  - Rules Check  │
                    │  - Fee Verify   │
                    │  - UTXO Exist   │
                    └─────────────────┘
```

### Core Components

#### 1. **Transaction Class** (`src/transaction.py`)
- Manages transaction inputs, outputs, and metadata
- Calculates transaction size and fee rates
- Implements realistic Bitcoin fee structure

#### 2. **UTXO Manager** (`src/utxo_manager.py`)
- Tracks all unspent transaction outputs
- Manages genesis block initialization
- Provides balance and UTXO lookup functions

#### 3. **Mempool** (`src/mempool.py`)
- Maintains pool of unconfirmed transactions
- Implements priority-based transaction ordering
- Prevents double-spending conflicts

#### 4. **Validator** (`src/validator.py`)
- Enforces Bitcoin transaction rules:
  - Input existence verification
  - Double-spend detection
  - Balance validation
  - Fee calculation

#### 5. **Mining Engine** (`src/mining.py`)
- Selects highest fee transactions
- Updates UTXO set after mining
- Distributes fees to miners

### Fee System Design

The simulator implements a realistic Bitcoin fee system:

- **Fee Rate**: Measured in satoshis per byte (sat/byte)
- **Transaction Size**: Calculated based on inputs/outputs
  - ~148 bytes per input
  - ~34 bytes per output
  - +10 bytes overhead
- **Total Fee**: Fee Rate × Transaction Size
- **Priority**: Higher fee rates get mined first

### Genesis Block
Initial UTXO distribution:
- Alice: 50 BTC
- Bob: 30 BTC
- Charlie: 20 BTC
- David: 10 BTC
- Eve: 5 BTC

## Test Suite

The simulator includes 10 comprehensive tests:

1. **Basic Valid Transaction** - Standard transaction with change and fees
2. **Multiple Inputs** - Aggregating multiple UTXOs
3. **Double-Spend in Same Transaction** - Invalid transaction rejection
4. **Mempool Double-Spend** - First-seen rule enforcement
5. **Insufficient Funds** - Balance validation
6. **Negative Amount** - Input validation
7. **Zero Fee Transaction** - Valid zero-fee handling
8. **Race Attack Simulation** - Attack prevention
9. **Complete Mining Flow** - End-to-end mining process
10. **Unconfirmed Chain** - Unconfirmed UTXO handling

##  Project Structure

```
Blockchain/
├── src/
│   ├── main.py              # Main application entry point
│   ├── transaction.py       # Transaction class and fee logic
│   ├── utxo_manager.py      # UTXO tracking and management
│   ├── mempool.py           # Transaction pool operations
│   ├── validator.py         # Transaction validation rules
│   └── mining.py            # Block mining simulation
├── test_scripts/
│   └── test_scenarios.py    # Comprehensive test suite
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

##  Limitations

- Simplified transaction ID generation (not cryptographic hashes)
- No network simulation or p2p communication
- No block headers or PoW consensus
- No script system or advanced transaction types
- Single-threaded execution model


## License

This project is created for educational purposes as part of CS 216 coursework.

---

**Note**: This simulator is designed for educational purposes to demonstrate Bitcoin transaction mechanics. It is not suitable for production use or real cryptocurrency operations.


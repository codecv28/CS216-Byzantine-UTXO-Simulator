from typing import List, Dict

class Transaction:
    def __init__(self, tx_id: str, inputs: List[Dict], outputs: List[Dict]):
        self.tx_id = tx_id
        self.inputs = inputs
        self.outputs = outputs
        self.fee = 0.0
        self.size_bytes = self.calculate_size()
        self.fee_rate = 0.0  # satoshis per byte
    
    def calculate_size(self) -> int:
        """
        Estimate transaction size in bytes (simplified Bitcoin calculation)
        Real Bitcoin: ~148 bytes per input + ~34 bytes per output + ~10 bytes overhead
        """
        # Simplified size calculation
        input_size = len(self.inputs) * 148  # Each input ~148 bytes
        output_size = len(self.outputs) * 34  # Each output ~34 bytes
        overhead = 10  # Transaction overhead
        
        return input_size + output_size + overhead
    
    def set_fee_rate(self, sat_per_byte: float):
        """Set fee rate and calculate total fee"""
        self.fee_rate = sat_per_byte
        # Convert satoshis to BTC (1 BTC = 100,000,000 satoshis)
        fee_in_satoshis = self.size_bytes * sat_per_byte
        self.fee = fee_in_satoshis / 100_000_000  # Convert to BTC

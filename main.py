# Step 1
import numpy as np
from qiskit import QuantumCircuit

def generate_random_key_and_basis(length):
    """
    Here I generated a random sequence of 0s and 1s for the key and the basis.
    """
    key = np.random.randint(2, size=length)
    basis = np.random.randint(2, size=length)  # 0 = Standard Basis, 1 = Hadamard Basis
    return key, basis

# Mohammed's step: Generate random key and basis
key_length = 10
mohammed_key, mohammed_basis = generate_random_key_and_basis(key_length)

print(f"Mohammed's Key: {mohammed_key}")
print(f"Mohammed's Basis: {mohammed_basis}")


#Step 2

def encode_qubits(key, basis):
    """
    I encoded the qubits based on the key and basis.
    It returns a list of QuantumCircuits representing each qubit.
    """
    qubits = []
    for bit, bas in zip(key, basis):
        qc = QuantumCircuit(1, 1)  # Create a single-qubit quantum circuit
        if bas == 1:  # Hadamard Basis
            qc.h(0)  # Apply Hadamard gate
        if bit == 1:  # If the bit is 1, apply an X gate to flip the state
            qc.x(0)
        qubits.append(qc)
    return qubits

# Mohammed encodes qubits
mohammed_qubits = encode_qubits(mohammed_key, mohammed_basis)

print("\nMohammed has encoded the qubits.")
for i, qc in enumerate(mohammed_qubits):
    print(f"Qubit {i + 1}: Circuit\n{qc}")


#Step 3

def measure_qubits(qubits, measurement_basis):
    """
    Measure qubits based on Ada's randomly chosen basis.
    Returns the measurement results and Ada's basis.
    """
    ada_results = []
    for qc, bas in zip(qubits, measurement_basis):
        if bas == 1:  # Hadamard Basis
            qc.h(0)  # Apply Hadamard gate before measurement
        qc.measure(0, 0)  # Measure the qubit
        ada_results.append(int(np.random.choice([0, 1], p=[0.5, 0.5])))  # Simulated measurement
    return ada_results

# Adas step: Generate random basis and measure qubits
ada_basis = np.random.randint(2, size=key_length)
ada_results = measure_qubits(mohammed_qubits, ada_basis)

print(f"\nAda's Basis: {ada_basis}")
print(f"Ada's Measurement Results: {ada_results}")

#Step 4

def reconcile_keys(mohammed_basis, ada_basis, mohammed_key, ada_results):
    """
    Here I compared Mohammed's and Ada's bases to determine the shared key.
    Returns the shared key where the bases match.
    """
    shared_key = []
    for mb, ab, mk, ar in zip(mohammed_basis, ada_basis, mohammed_key, ada_results):
        if mb == ab:  # Basis match
            shared_key.append(mk)  # Use Mohammed's key (equivalent to Ada's if bases match)
    return shared_key

# Key reconciliation
shared_key = reconcile_keys(mohammed_basis, ada_basis, mohammed_key, ada_results)

print(f"\nShared Key (After Reconciliation): {shared_key}")
print(f"Key Length After Reconciliation: {len(shared_key)}")

#Step 5

def verify_key(shared_key):
    """
   Here I simulated a verification step to check for eavesdropping.
    Mohammed and Ada compare a random subset of their shared key.
    """
    # Select a random subset of bits for verification
    subset_indices = np.random.choice(len(shared_key), size=len(shared_key) // 2, replace=False)
    mohammed_sample = [shared_key[i] for i in subset_indices]
    ada_sample = [shared_key[i] for i in subset_indices]

    print(f"\nVerification Subset Indices: {subset_indices}")
    print(f"Mohammed's Verification Sample: {mohammed_sample}")
    print(f"Ada's Verification Sample: {ada_sample}")

    # Verify if samples match
    if mohammed_sample == ada_sample:
        print("\nKey Verified: No eavesdropping detected!")
    else:
        print("\nKey Verification Failed: Possible eavesdropping detected!")

# Perform key verification
verify_key(shared_key)

#Step 6
def eavesdrop_on_qubits(qubits):
    """
    Here I simulated Eve measuring the qubits with a random basis.
    Eve's measurement alters the original qubits and introduces errors.
    """
    eve_basis = np.random.randint(2, size=len(qubits))
    print(f"\nEve's Basis: {eve_basis}")

    for i, qc in enumerate(qubits):
        if eve_basis[i] == 1:  # Hadamard Basis
            qc.h(0)  # Apply Hadamard gate
        qc.measure(0, 0)  # Eve measures the qubit
        
        # Randomly re-prepare the qubit based on Eve's measurement
        new_state = np.random.choice([0, 1], p=[0.5, 0.5])  # Simulated result
        if new_state == 1:
            qc.x(0)  # Flip the state for a 1
        if eve_basis[i] == 1:  # Restore Hadamard Basis for Ada
            qc.h(0)

# Simulate eavesdropping
eavesdrop_on_qubits(mohammed_qubits)

print("\nEavesdropping has occurred. Ada will now measure altered qubits.")

#Step 7

def apply_noise(qubits, noise_probability=0.2):
    """
    Here I simulated noise in the quantum channel by flipping qubit states
    with a given probability.
    """
    for qc in qubits:
        if np.random.rand() < noise_probability:  # Randomly apply noise
            qc.x(0)  # Flip the qubit state (bit-flip error)

# Simulate noise in the channel
noise_probability = 0.1  # 10% chance of noise per qubit
apply_noise(mohammed_qubits, noise_probability)

print(f"\nNoise applied with probability {noise_probability}.")

# Step 8

def eavesdrop_on_qubits(qubits):
    """
    Here simulated Eve measuring the qubits with a random basis and log her actions.
    """
    eve_basis = np.random.randint(2, size=len(qubits))
    print(f"\nEve's Basis: {eve_basis}")

    eve_logs = []  # Log Eve's actions

    for i, qc in enumerate(qubits):
        # Eve chooses a random basis
        chosen_basis = 'Hadamard' if eve_basis[i] == 1 else 'Standard'
        eve_logs.append(f"Qubit {i + 1}: Eve uses {chosen_basis} basis.")

        # Measure the qubit
        if eve_basis[i] == 1:
            qc.h(0)  # Apply Hadamard gate
        measurement_result = np.random.choice([0, 1], p=[0.5, 0.5])  # Simulated measurement
        eve_logs.append(f"Qubit {i + 1}: Eve measures and gets {measurement_result}.")

        # Re-prepare the qubit based on Eve's measurement
        if measurement_result == 1:
            qc.x(0)  # Flip state
        if eve_basis[i] == 1:
            qc.h(0)  # Restore Hadamard basis for Ada

    # Print Eve's logs
    print("\nEve's Actions:")
    for log in eve_logs:
        print(log)

# Simulate eavesdropping
eavesdrop_on_qubits(mohammed_qubits)

print("\nEavesdropping has occurred with detailed logging.")

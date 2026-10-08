
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    thermal_relaxation_error,
)

# Hardware parameters in microseconds
T1 = 80.0
T2 = 60.0

# Simulation settings
shots = 4096
times = np.linspace(0, 200, 41)

simulator = AerSimulator()
results = []

for duration in times:
    # Build a quantum circuit
    qc = QuantumCircuit(1, 1)

    # Prepare excited state |1>
    qc.x(0)

    # Idle period represented by an identity gate
    qc.id(0)

    # Measure the qubit
    qc.measure(0, 0)

    # Thermal relaxation during the idle period
    error = thermal_relaxation_error(
        t1=T1,
        t2=T2,
        time=float(duration),
    )

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error, ["id"])

    # Run noisy circuit
    job = simulator.run(
        qc,
        noise_model=noise_model,
        shots=shots,
    )

    counts = job.result().get_counts()

    probability_one = counts.get("1", 0) / shots
    results.append(probability_one)

# Theoretical excited-state survival probability
theory = np.exp(-times / T1)

# Plot results
plt.figure(figsize=(11, 6))

plt.plot(
    times,
    theory,
    label="T1 theoretical decay",
    linewidth=2.5,
)

plt.scatter(
    times,
    results,
    label="Qiskit Aer simulation",
    s=35,
)

plt.title("Quantum Hardware - Thermal Relaxation")
plt.xlabel("Idle time (microseconds)")
plt.ylabel("Probability of measuring |1>")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig("thermal_noise_results.png", dpi=200)
plt.show()

print("Thermal Relaxation Simulation Complete")
print(f"T1: {T1} microseconds")
print(f"T2: {T2} microseconds")
print(f"Shots per experiment: {shots}")
print("Graph saved: thermal_noise_results.png")


import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error

# Hardware parameters (microseconds)
T1 = 80.0
T2 = 60.0

# Simulation settings
SHOTS = 4096
times = np.linspace(0, 200, 41)

simulator = AerSimulator()
measured_probabilities = []

for duration in times:
    # Ramsey-style coherence measurement
    qc = QuantumCircuit(1, 1)

    # Prepare |+> superposition
    qc.h(0)

    # Simulated idle time
    qc.id(0)

    # Convert coherence into population
    qc.h(0)

    # Measure
    qc.measure(0, 0)

    # Thermal relaxation and dephasing
    noise_model = NoiseModel()

    error = thermal_relaxation_error(
        t1=T1,
        t2=T2,
        time=float(duration),
    )

    noise_model.add_all_qubit_quantum_error(
        error,
        ["id"],
    )

    result = simulator.run(
        qc,
        noise_model=noise_model,
        shots=SHOTS,
    ).result()

    counts = result.get_counts()
    probability_zero = counts.get("0", 0) / SHOTS

    measured_probabilities.append(probability_zero)

# Ramsey coherence model
theoretical_coherence = np.exp(-times / T2)
theoretical_probability_zero = (
    1 + theoretical_coherence
) / 2

# Visualization
plt.figure(figsize=(11, 6))

plt.plot(
    times,
    theoretical_probability_zero,
    label="Theoretical Ramsey signal",
    linewidth=2.5,
)

plt.scatter(
    times,
    measured_probabilities,
    label="Qiskit Aer simulation",
    s=35,
)

plt.axhline(
    0.5,
    color="gray",
    linestyle=":",
    label="Fully decohered limit",
)

plt.title("Quantum Hardware - T2 Ramsey Experiment")
plt.xlabel("Idle time (microseconds)")
plt.ylabel("Probability of measuring |0>")
plt.ylim(0.45, 1.05)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig("ramsey_results.png", dpi=200)
plt.show()

print("T2 Ramsey Experiment Complete")
print(f"T1 = {T1} microseconds")
print(f"T2 = {T2} microseconds")
print(f"Shots = {SHOTS}")
print("Graph saved: ramsey_results.png")

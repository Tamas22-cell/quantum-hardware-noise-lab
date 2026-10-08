
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    depolarizing_error,
    ReadoutError,
)

SHOTS = 4096
ERROR_RATES = np.linspace(0, 0.20, 21)

simulator = AerSimulator()
ideal_results = []
gate_results = []
readout_results = []
combined_results = []

# Prepare |1> using an X gate
qc = QuantumCircuit(1, 1)
qc.x(0)
qc.measure(0, 0)


def simulate(gate_error=0.0, readout_error=0.0):
    noise_model = NoiseModel()

    if gate_error > 0:
        noise_model.add_all_qubit_quantum_error(
            depolarizing_error(gate_error, 1),
            ["x"],
        )

    if readout_error > 0:
        measurement_error = ReadoutError([
            [1 - readout_error, readout_error],
            [readout_error, 1 - readout_error],
        ])

        noise_model.add_all_qubit_readout_error(
            measurement_error
        )

    result = simulator.run(
        qc,
        noise_model=noise_model,
        shots=SHOTS,
    ).result()

    counts = result.get_counts()
    return counts.get("1", 0) / SHOTS


for error_rate in ERROR_RATES:
    ideal_results.append(1.0)

    gate_results.append(
        simulate(gate_error=float(error_rate))
    )

    readout_results.append(
        simulate(readout_error=float(error_rate))
    )

    combined_results.append(
        simulate(
            gate_error=float(error_rate),
            readout_error=float(error_rate),
        )
    )

plt.figure(figsize=(11, 6))

plt.plot(
    ERROR_RATES * 100,
    ideal_results,
    label="Ideal circuit",
    linestyle="--",
)

plt.plot(
    ERROR_RATES * 100,
    gate_results,
    marker="o",
    label="Gate noise",
)

plt.plot(
    ERROR_RATES * 100,
    readout_results,
    marker="s",
    label="Readout error",
)

plt.plot(
    ERROR_RATES * 100,
    combined_results,
    marker="^",
    label="Combined noise",
)

plt.title("Quantum Hardware - Gate and Readout Noise")
plt.xlabel("Error parameter (%)")
plt.ylabel("Probability of measuring |1>")
plt.ylim(0.65, 1.03)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig("gate_readout_results.png", dpi=200)
plt.show()

print("Gate and Readout Noise Simulation Complete")
print(f"Shots per experiment: {SHOTS}")
print("Graph saved: gate_readout_results.png")


import numpy as np
import matplotlib.pyplot as plt

# Quantum hardware parameters (microseconds)
T1 = 80.0
T2 = 60.0

# Simulation time
time = np.linspace(0, 200, 500)

# T1: energy relaxation
excited_population = np.exp(-time / T1)

# T2: coherence decay
coherence = np.exp(-time / T2)

# Theoretical constraint: T2 <= 2*T1
if T2 > 2 * T1:
    raise ValueError("T2 cannot exceed 2*T1.")

# Create visualization
plt.figure(figsize=(11, 6))

plt.plot(
    time,
    excited_population,
    label=f"T1 Relaxation ({T1} us)",
    linewidth=2.5,
)

plt.plot(
    time,
    coherence,
    label=f"T2 Coherence Decay ({T2} us)",
    linewidth=2.5,
    linestyle="--",
)

plt.title("Quantum Hardware - T1 and T2 Noise Simulation")
plt.xlabel("Time (microseconds)")
plt.ylabel("Normalized population / coherence")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig("t1_t2_results.png", dpi=200)
plt.show()

print("Quantum Hardware Noise Simulation")
print(f"T1 relaxation time: {T1} microseconds")
print(f"T2 coherence time: {T2} microseconds")
print("Graph saved: t1_t2_results.png")

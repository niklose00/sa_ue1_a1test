# glowworm_debug_v2.py

from glowworm import Glowworm
import random
import math
import threading
import time

# Hinzufügen einer eindeutigen ID für jedes Glowworm für bessere Nachverfolgbarkeit
class DebugGlowworm(Glowworm):
    _id_counter = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = DebugGlowworm._id_counter
        DebugGlowworm._id_counter += 1

    def __repr__(self):
        return f"Glowworm(ID: {self.id}, Phase: {self.phase:.2f}, Neighbors: {len(self.neighbors)})"

# Erzeuge mehrere Debug-Glowworms
def create_glowworms(num_glowworms):
    glowworms = [DebugGlowworm(natural_frequency=random.uniform(0.8, 1.2)) for _ in range(num_glowworms)]
    for i, glowworm in enumerate(glowworms):
        glowworm.neighbors = [g for j, g in enumerate(glowworms) if i != j]
    return glowworms

def simulate(num_glowworms=5, steps=5):
    glowworms = create_glowworms(num_glowworms)

    print("Initialer Zustand der Glowworms:")
    for g in glowworms:
        print(g)
    print("\nSimulation startet...")

    for step in range(steps):
        print(f"\n--- Schritt {step + 1} ---")
        for glowworm in glowworms:
            glowworm.update_phase()
            # Anzeigen der Phase und Einfluss der Nachbarn für jedes Glowworm
            print(f"Glowworm ID {glowworm.id}: Neue Phase = {glowworm.phase:.2f}")
            for neighbor in glowworm.neighbors:
                print(f"  Einfluss von Nachbar ID {neighbor.id}, Phase: {neighbor.phase:.2f}")

        # Grad der Synchronisation (Beispiel: nur Mittelwert)
        phases = [g.phase for g in glowworms]
        sync_ratio = sum(math.cos(phase) for phase in phases) / len(glowworms)
        print(f"\nGrad der Synchronisation (r): {sync_ratio:.2f}")

        time.sleep(0.5)  # Simulation Pause für Klarheit

    print("\nSimulation beendet.")
    print("Endzustand der Glowworms:")
    for g in glowworms:
        print(g)

simulate()

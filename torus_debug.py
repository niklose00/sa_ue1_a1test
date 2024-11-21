# torus_debug.py
import time
from torus import Torus

def debug_torus_simulation(rows, cols, coupling_strength, steps=5):
    torus = Torus(rows=rows, cols=cols, coupling_strength=coupling_strength)
    torus.start()

    print("Initialer Zustand des Torus:")
    print(torus)
    print("\nSimulation startet...\n")

    try:
        for step in range(steps):
            print(f"--- Schritt {step + 1} ---")
            print(torus)  # Gibt die aktuelle Phasenmatrix des Torus aus

            # Berechne und zeige den Synchronisationsgrad
            sync_degree = torus.degree_of_synchronization()
            print(f"Grad der Synchronisation (r): {sync_degree:.2f}")

            # Überprüfen Sie den Status der Threads
            print("Thread-Status der Glühwürmchen:")
            for row in range(torus.rows):
                for col in range(torus.cols):
                    glowworm = torus.grid[row][col]
                    if glowworm.thread.is_alive():
                        print(f"Glühwürmchen ({row}, {col}) läuft.")
                    else:
                        print(f"Glühwürmchen ({row}, {col}) gestoppt.")

            time.sleep(1)  # Kurze Pause zwischen den Schritten

    finally:
        # Stoppe alle Threads, sobald die Simulation beendet ist
        torus.stop()
        print("\nSimulation beendet.")
        print("Endzustand des Torus:")
        print(torus)

# Simulation mit 3x3 Torus und Kopplungsstärke 1.0 über 5 Schritte
if __name__ == "__main__":
    debug_torus_simulation(rows=3, cols=3, coupling_strength=1.0, steps=100)

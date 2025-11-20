Epidemic Spread Simulation (Interactive SIR Model)
=================================================

Run an interactive simulation of an SIR epidemic with moving agents.
Sliders let you change population size, infection probability, recovery time,
vaccination rate, and movement speed. A lockdown checkbox reduces movement speed.
The program shows an animated scatter of agents and a live S/I/R plot.

Requirements:
  - Python 3.8+ (3.10 or 3.11 recommended)
  - Install dependencies in a venv:
      python -m venv .venv
      source .venv/bin/activate   # or .venv\Scripts\activate on Windows
      pip install -r requirements.txt

Run:
  python src/main.py

Files:
  src/simulation.py  - core SIR simulation & agent model
  src/visualize.py   - interactive matplotlib UI (sliders/buttons)
  src/main.py        - launches the interactive UI

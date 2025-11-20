
import argparse
from visualize import launch_interactive

def parse_args():
    ap = argparse.ArgumentParser(description='Interactive SIR Epidemic Simulation')
    ap.add_argument('--population', type=int, default=200)
    ap.add_argument('--infection_prob', type=float, default=0.25)
    ap.add_argument('--recovery_time', type=int, default=50)
    ap.add_argument('--vacc', type=float, default=0.0)
    ap.add_argument('--speed', type=float, default=1.0)
    ap.add_argument('--lockdown', action='store_true')
    return ap.parse_args()

def main():
    args = parse_args()
    launch_interactive(population=args.population,
                       infection_prob=args.infection_prob,
                       recovery_time=args.recovery_time,
                       vacc_percent=args.vacc,
                       speed=args.speed,
                       lockdown=args.lockdown)

if __name__ == '__main__':
    main()


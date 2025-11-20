import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, CheckButtons
import math
from simulation import SIRSimulation

class InteractiveSIR:
    def __init__(self, sim=None, width=8, height=6):
        self.sim = sim or SIRSimulation()
        self.fig = plt.figure(figsize=(width, height))

        
        self.ax_grid = self.fig.add_axes([0.05, 0.38, 0.55, 0.57])   
        self.ax_plot = self.fig.add_axes([0.65, 0.38, 0.30, 0.57])   

        
        left1, left2 = 0.08, 0.55     
        bottom_start = 0.12
        h = 0.03
        gap = 0.06
        w = 0.30                                                         

        self.ax_pop      = self.fig.add_axes([left1, bottom_start + 2*gap, w, h])
        self.ax_infprob  = self.fig.add_axes([left1, bottom_start + 1*gap, w, h])
        self.ax_recovery = self.fig.add_axes([left1, bottom_start + 0*gap, w, h])

        self.ax_vacc     = self.fig.add_axes([left2, bottom_start + 2*gap, w, h])
        self.ax_speed    = self.fig.add_axes([left2, bottom_start + 1*gap, w, h])

        # Lockdown button and Reset button, placed below/right of sliders
        self.ax_lockbtn  = self.fig.add_axes([left2, bottom_start - 0.01, 0.15, 0.045])
        self.ax_reset    = self.fig.add_axes([0.78, bottom_start + 0.03, 0.10, 0.045])

        # ------------------------------------------------------------------
        # Sliders
        # ------------------------------------------------------------------
        self.s_pop = Slider(self.ax_pop, 'Population', 20, 800,
                            valinit=self.sim.population,valstep=1)
        self.s_inf = Slider(self.ax_infprob, 'InfectProb', 0.0, 1.0,
                            valinit=self.sim.infection_prob)
        self.s_rec = Slider(self.ax_recovery, 'Recovery', 1, 200,
                            valinit=self.sim.recovery_time, valstep=1)
        self.s_vacc = Slider(self.ax_vacc, 'Vacc%', 0.0, 0.95,
                             valinit=self.sim.vacc_percent, valstep=0.01)
        self.s_speed = Slider(self.ax_speed, 'Speed', 0.0, 5.0,
                              valinit=self.sim.speed)

        # Buttons / Checkboxes
        self.chk = CheckButtons(self.ax_lockbtn, ['Lockdown'], [self.sim.lockdown])
        self.btn_reset = Button(self.ax_reset, 'Reset')

        # scatter and lines
        self.scatter = None
        self.lineS, = self.ax_plot.plot([], [], label='S')
        self.lineI, = self.ax_plot.plot([], [], label='I')
        self.lineR, = self.ax_plot.plot([], [], label='R')
        self.ax_plot.set_xlim(0, 200)
        self.ax_plot.set_ylim(0, max(10, self.sim.population))
        self.ax_plot.set_xlabel('Time')
        self.ax_plot.set_ylabel('Count')
        self.ax_plot.legend(loc='upper right')

        # connect events
        self.s_pop.on_changed(self.on_param_change)
        self.s_inf.on_changed(self.on_param_change)
        self.s_rec.on_changed(self.on_param_change)
        self.s_vacc.on_changed(self.on_param_change)
        self.s_speed.on_changed(self.on_param_change)
        self.chk.on_clicked(self.on_lock_change)
        self.btn_reset.on_clicked(self.on_reset)

        # animation
        self.ani = FuncAnimation(self.fig, self._update, interval=80, blit=False)
        plt.show()

    def on_param_change(self, val):
        # update sim parameters but don't destroy sim until reset
        self.sim.infection_prob = float(self.s_inf.val)
        self.sim.recovery_time = int(self.s_rec.val)
        self.sim.vacc_percent = float(self.s_vacc.val)
        self.sim.speed = float(self.s_speed.val)
        # update plot ylim/population
        pop = int(self.s_pop.val)
        self.ax_plot.set_ylim(0, max(10, pop))
        self.ax_plot.set_xlim(0, max(200, 5 * pop // 10))

    def on_lock_change(self, labels):
        # toggle lockdown: change speed multiplier
        self.sim.lockdown = not self.sim.lockdown
        for a in self.sim.agents:
            if self.sim.lockdown:
                a.vx *= 0.2
                a.vy *= 0.2
            else:
                # scale back to base speed slider
                factor = self.sim.speed / max(1e-6, math.hypot(a.vx, a.vy))
                a.vx *= factor * 0.8
                a.vy *= factor * 0.8

    def on_reset(self, event):
        # rebuild sim with current slider params
        p = int(self.s_pop.val)
        infp = float(self.s_inf.val)
        rec = int(self.s_rec.val)
        vacc = float(self.s_vacc.val)
        spd = float(self.s_speed.val)
        lock = self.sim.lockdown
        self.sim = SIRSimulation(population=p, width=100, height=100,
                                 infection_radius=2.0, infection_prob=infp,
                                 recovery_time=rec, vacc_percent=vacc,
                                 seed=None, speed=spd, lockdown=lock)
        # clear plot history
        self.lineS.set_data([], [])
        self.lineI.set_data([], [])
        self.lineR.set_data([], [])
        self.ax_plot.set_ylim(0, max(10, p))
        self.ax_plot.set_xlim(0, max(200, 5 * p // 10))

    def _update(self, frame):
        # advance simulation some steps per animation tick for speed
        for _ in range(1):
            self.sim.step()
        xs = [a.x for a in self.sim.agents]
        ys = [a.y for a in self.sim.agents]
        states = [a.state for a in self.sim.agents]

        # scatter plotting: color by state using default color cycle
        colors = []
        sizes = []
        for s in states:
            if s == 0:
                colors.append('C0')  # susceptible
                sizes.append(10)
            elif s == 1:
                colors.append('C1')  # infected
                sizes.append(20)
            else:
                colors.append('C2')  # recovered
                sizes.append(10)

        self.ax_grid.clear()
        self.ax_grid.set_xlim(0, self.sim.width)
        self.ax_grid.set_ylim(0, self.sim.height)
        self.ax_grid.scatter(xs, ys, s=sizes, c=colors)
        self.ax_grid.set_title(f'Time: {self.sim.time}')

        # update SIR lines
        t = list(range(len(self.sim.history['S'])))
        self.lineS.set_data(t, self.sim.history['S'])
        self.lineI.set_data(t, self.sim.history['I'])
        self.lineR.set_data(t, self.sim.history['R'])

        return []

def launch_interactive(**kwargs):
    sim = SIRSimulation(**kwargs)
    ui = InteractiveSIR(sim=sim)
    return ui

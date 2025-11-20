
import random, math
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

class Agent:
    def __init__(self, x, y, vx, vy, state=SUSCEPTIBLE, infected_time=0):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.state = state
        self.infected_time = infected_time

    def step(self, dt=1.0, bounds=(100,100)):
        self.x += self.vx * dt
        self.y += self.vy * dt
        w, h = bounds
        # bounce off walls
        if self.x < 0:
            self.x = -self.x
            self.vx = -self.vx
        if self.x > w:
            self.x = 2*w - self.x
            self.vx = -self.vx
        if self.y < 0:
            self.y = -self.y
            self.vy = -self.vy
        if self.y > h:
            self.y = 2*h - self.y
            self.vy = -self.vy

class SIRSimulation:
    def __init__(self, population=200, width=100, height=100,
                 infection_radius=2.0, infection_prob=0.3, recovery_time=50,
                 vacc_percent=0.0, seed=None, speed=1.0, lockdown=False):
        import random, math
        self.rng = random.Random(seed)
        self.population = int(population)
        self.width = width
        self.height = height
        self.infection_radius = float(infection_radius)
        self.infection_prob = float(infection_prob)
        self.recovery_time = int(recovery_time)
        self.vacc_percent = float(vacc_percent)
        self.speed = float(speed)
        self.lockdown = bool(lockdown)

        self.agents = []
        self.time = 0
        self.history = {'S':[], 'I':[], 'R':[]}
        self._init_agents()

    def _init_agents(self):
        self.agents = []
        for i in range(self.population):
            x = self.rng.uniform(0, self.width)
            y = self.rng.uniform(0, self.height)
            angle = self.rng.uniform(0, 2*math.pi)
            sp = self.speed * (0.2 if self.lockdown else 1.0)
            vx = math.cos(angle) * sp * self.rng.uniform(0.5, 1.0)
            vy = math.sin(angle) * sp * self.rng.uniform(0.5, 1.0)
            # vaccination: set some initially recovered (immune)
            if self.rng.random() < self.vacc_percent:
                state = RECOVERED
            else:
                state = SUSCEPTIBLE
            agent = Agent(x, y, vx, vy, state=state)
            self.agents.append(agent)
        # seed one infected (unless all vaccinated)
        susceptibles = [a for a in self.agents if a.state == SUSCEPTIBLE]
        if susceptibles:
            patient_zero = self.rng.choice(susceptibles)
            patient_zero.state = INFECTED
            patient_zero.infected_time = 0

        self.time = 0
        self.history = {'S':[], 'I':[], 'R':[]}
        self._record()

    def step(self):
        dt = 1.0
        # move agents
        for a in self.agents:
            a.step(dt=dt, bounds=(self.width, self.height))

        # infection process: naive O(n^2) check (fine for <=200-1000 agents)
        for i, ai in enumerate(self.agents):
            if ai.state == INFECTED:
                for j, aj in enumerate(self.agents):
                    if aj.state == SUSCEPTIBLE:
                        dx = ai.x - aj.x
                        dy = ai.y - aj.y
                        if dx*dx + dy*dy <= (self.infection_radius ** 2):
                            if self.rng.random() < self.infection_prob:
                                aj.state = INFECTED
                                aj.infected_time = 0

        # recoveries
        for a in self.agents:
            if a.state == INFECTED:
                a.infected_time += 1
                if a.infected_time >= self.recovery_time:
                    a.state = RECOVERED

        self.time += 1
        self._record()

    def _record(self):
        s = sum(1 for a in self.agents if a.state == 0)
        i = sum(1 for a in self.agents if a.state == 1)
        r = sum(1 for a in self.agents if a.state == 2)
        self.history['S'].append(s)
        self.history['I'].append(i)
        self.history['R'].append(r)

    def run(self, steps=200):
        for _ in range(steps):
            self.step()
        return self.history


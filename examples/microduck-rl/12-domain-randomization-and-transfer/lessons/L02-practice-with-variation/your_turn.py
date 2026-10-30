"""YOUR DESIGN: which conditions should the robot practise in?

Each entry is either one number (every robot gets exactly that) or a (low, high)
range (each practising robot gets its own random value from it).

  voltage      motor supply voltage, volts        (nominal robot: 7.4)
  friction     foot-ground friction coefficient   (nominal robot: 1.0)
  delay_steps  command delay in 5 ms steps        (nominal robot: 4)

Ideas to try: widen one range a lot; randomize everything; randomize nothing.
What do you gain on unusual robots, and what does it cost on the normal one?
"""


def practice_conditions():
    return {
        "delay_steps": (2, 12),
        "friction": (0.2, 1.2),
        "voltage": (4.5, 8.2),
    }

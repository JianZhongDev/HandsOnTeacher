# Credits

HandsOnTeacher is released under the [MIT License](LICENSE).

## Where the method comes from

- **[Learn RL with MicroDuck](https://github.com/JianZhongDev/LearnRLWithMicroDuck)** (MIT, same author). The teaching rules, skills, writing guide, lab helpers (`kit/handson`, adapted from its `duckkit`) and the worked example in `examples/microduck-rl/` come from building and trial-teaching that course.
- **[MicroDuck](https://github.com/pollen-robotics/microduck)** and **[microduck_rl](https://github.com/pollen-robotics/microduck_rl)** by [Pollen Robotics](https://github.com/pollen-robotics) (Apache-2.0): the codebase that course teaches with. The worked example describes their design and quotes no code. The figures in `examples/microduck-rl/` are diagrams drawn by the course's own code, not renderings of the robot.
- J. Tobin et al. *Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World.* IROS 2017. Cited by the example lesson.

## Formats and conventions

- [Agent Skills](https://agentskills.io/) layout (`.agents/skills/<name>/SKILL.md` with `scripts/`, `references/`, `assets/`) and the [AGENTS.md](https://agents.md/) convention for agent instructions.

## Tools the kit and courses use

- [Python](https://www.python.org/) (PSF License), [Matplotlib](https://matplotlib.org/) (Matplotlib License), [Pillow](https://python-pillow.org/) (MIT-CMU), [uv](https://docs.astral.sh/uv/) (Apache-2.0 or MIT). Each course's codebase keeps its own license: the agent records it in `course.json` and quotes only what lessons need.

"""<MM>.L<nn>: <question>. Runs <the codebase's thing> under <N> settings side by side.

Run: lab <MM>/L<nn>      Tweak: lab <MM>/L<nn> <knob>=<value>      Design: edit your_turn.py
"""
import handson as ho

run = ho.lab_config({"<knob>": 1.0, "size": 1000},
                    help={"<knob>": "<meaning, units>", "size": "<how much input, units>"})

from your_turn import my_version          # the learner's design (a working default is provided)
# from <codebase> import <the thing>      # the real codebase, read-only


def measure(variant) -> dict:
    """Run one variant on the same input; return what a user would notice."""
    with ho.timed() as t:
        result = variant(run.cfg.size)    # replace with the real call
    return {"<observable metric>": result, "time (s)": t.seconds}


rows = {
    "codebase default": measure(lambda n: n),   # replace with the codebase's own version
    "your version": measure(my_version),
}
ho.print_table(rows)
run.save_json("metrics.json", rows)

# One picture with every setting on the same axes (needs matplotlib):
ho.use_style()
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.bar(list(rows), [r["time (s)"] for r in rows.values()])
ax.set(ylabel="time (s)", title="<the question, answered at a glance>")
ho.save_fig(fig, run.out / "compare.png")

# handson kit quick reference

Location in a course: `courses/<course>/_shared/handson/` (copied from `kit/handson/` by `tools/new_course.py`; the launcher puts `_shared/` on `PYTHONPATH`). Importing it needs only the Python standard library; plotting needs matplotlib, `side_by_side` needs Pillow.

```python
import handson as ho
```

## Settings and results: `handson.labkit`

```python
run = ho.lab_config(defaults: dict, help: dict) -> LabRun
run.cfg.<name>      # values after key=value overrides from the command line
run.changed         # settings that differ from the defaults
run.out             # results/<default | key=value,...>/  (created; settings.json written)
run.lab_dir         # folder containing the lab file
run.save_json(name, data)
run.other_runs()    # result folders of earlier runs, for comparisons
```

`lab 03/L01 help` prints the settings and their help text.

## Comparing: `handson.compare`

```python
ho.reading_guide({"p95 latency (ms)": "time under which 95% of requests finish; lower is better"})   # legend BEFORE the results
ho.print_table({"setting A": {"p95 latency (ms)": 412, "errors": 0}, "setting B": {...}})
ho.side_by_side(["a.png", "b.png"], ["setting A", "setting B"], run.out / "compare.png")   # Pillow
with ho.timed() as t:
    work()
t.seconds
```

## Exploring: `handson.explore`

```python
ho.slider_page(run.out / "explore.html", title, slider_label, slider_values, x,
               {"curve name": [curve for each slider value]}, xlabel, ylabel,
               note="Drag the slider: ...")   # self-contained HTML, opens in any browser
```

Use it whenever the curves for several values of one setting compute in seconds.

## Pictures: `handson.viz` (matplotlib)

```python
ho.use_style()
ho.flow_diagram([("Title", "subtitle"), ...], highlight=[i], highlight_tag="TODAY",
                loop_label=None, edge_labels=None, title="", path=None)   # pipelines: module and course maps
ho.layer_diagram([("Applications", "programs you run"), ("Operating system", "..."), ...],
                 highlight=1, side_labels=["M02", "M03-M05", ...], title="", path=None)  # layered course maps
ho.save_fig(fig, path)
ho.COLORS, ho.SERIES
```

## Labs in other languages

Labs follow the same contract in any language, so the launcher and the learner's habits stay the same:

- The launcher runs `<runtime> <lab file> key=value ...` inside the lesson folder (`RUN` and `LAB_FILE` in `lab.sh` / `lab.cmd`).
- `help` as the only argument prints each setting, its default and its meaning, then exits.
- Unknown keys are an error that lists the known ones.
- Results go to `results/default/` or `results/<key=value,...>/`, with a `settings.json` of the values used.
- Output is one small table, plus a picture or a Markdown table file in the results folder.

Write a small helper with these functions once per course, in the course's `_shared/`, and import it from every lab.

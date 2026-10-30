"""handson: small helpers for hands-on labs. Copied into each course as `_shared/handson/`.

    import handson as ho
    run = ho.lab_config({"size": 1000, "policy": "lru"}, help={"size": "number of requests"})
    ...
    ho.print_table({"no cache": {...}, "LRU": {...}})

Modules:
    handson.labkit   lab_config: key=value settings from the command line, one results folder per setting
    handson.compare  print_table, side_by_side (Pillow), timed
    handson.explore  slider_page: a self-contained HTML page with a slider, for instant what-if exploration
    handson.viz      use_style, save_fig, flow_diagram (maps), layer_diagram (layered course maps); needs matplotlib
    handson.colors   COLORS, SERIES

Importing handson needs only the standard library. The plotting helpers need matplotlib and
side_by_side needs Pillow; each is imported only when used.
"""

from handson.colors import COLORS, SERIES
from handson.compare import print_table, side_by_side, timed
from handson.explore import slider_page
from handson.labkit import LabRun, lab_config


def __getattr__(name):
    # matplotlib is slow to import and optional: load the plotting helpers on first use.
    if name in {"use_style", "save_fig", "flow_diagram", "layer_diagram"}:
        from handson import viz

        return getattr(viz, name)
    raise AttributeError(name)


__all__ = ["lab_config", "LabRun", "print_table", "side_by_side", "timed", "slider_page",
           "use_style", "save_fig", "flow_diagram", "layer_diagram", "COLORS", "SERIES"]

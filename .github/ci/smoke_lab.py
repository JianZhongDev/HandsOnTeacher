"""CI fixture: the smallest lab, to test the launchers on each operating system."""
import handson as ho

run = ho.lab_config({"size": 3}, help={"size": "number of items"})
ho.print_table({"default": {"size": run.cfg.size}})
run.save_json("metrics.json", {"size": run.cfg.size})

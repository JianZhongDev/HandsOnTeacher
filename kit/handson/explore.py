"""One-file HTML pages with a slider, for instant what-if exploration.

A lab computes the curves for several values of one setting (fast things: a cost
function over a recorded run, a controller's step response, a noise level), then
writes a page. The learner drags the slider in a browser and sees the curves change
at once: no re-running, no server, no internet.

    slider_page(run.out / "explore.html", "Jerk penalty weight",
                   slider_label="weight", slider_values=[0, -0.1, -1, -5],
                   x=time_s, series={"reward": [curve_for_each_weight, ...]},
                   xlabel="time (s)", ylabel="reward per step",
                   note="Drag the slider: how much does a jerky step cost?")
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

from handson.colors import COLORS, SERIES

_PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<style>body{{font-family:system-ui,sans-serif;margin:24px;color:#1f2933;max-width:960px}}
h1{{font-size:22px;margin:0 0 6px}} .note{{color:#52606d;margin:0 0 14px}}
.row{{display:flex;gap:14px;align-items:center;margin:8px 0 12px;flex-wrap:wrap}} input[type=range]{{width:min(420px,60vw)}}
.val{{font-weight:600;font-size:18px}} canvas{{border:1px solid #e4e7eb;border-radius:8px;width:100%;height:auto;max-width:900px}}
.legend span{{margin-right:16px}} .legend i{{display:inline-block;width:14px;height:4px;margin-right:6px;vertical-align:middle}}
</style></head><body>
<h1>{title}</h1><p class="note">{note}</p>
<div class="row"><label>{slider_label}</label><input id="s" type="range" min="0" max="{last}" step="1" value="{start}">
<span class="val" id="v"></span></div>
<canvas id="c" width="900" height="420"></canvas><div class="legend" id="lg"></div>
<script>
const D={data};
const c=document.getElementById('c'),g=c.getContext('2d'),s=document.getElementById('s');
const L=78,R=20,T=16,B=50,W=c.width-L-R,H=c.height-T-B;
let ys=[];for(const k in D.series)for(const arr of D.series[k])ys=ys.concat(arr.filter(v=>v!==null));
const x0=Math.min(...D.x),x1=Math.max(...D.x);
let y0=D.ylim?D.ylim[0]:Math.min(...ys),y1=D.ylim?D.ylim[1]:Math.max(...ys);if(y0===y1){{y0-=1;y1+=1}}
const pad=(y1-y0)*0.06;if(!D.ylim){{y0-=pad;y1+=pad}}
const X=v=>L+(v-x0)/(x1-x0||1)*W, Y=v=>T+(1-(v-y0)/(y1-y0))*H;
function nice(a,b,n){{const st=Math.pow(10,Math.floor(Math.log10((b-a)/n)));const m=[1,2,5,10].find(m=>(b-a)/(st*m)<=n)*st;
 const out=[];for(let v=Math.ceil(a/m)*m;v<=b+1e-12;v+=m)out.push(+v.toPrecision(6));return out}}
function draw(){{const i=+s.value;document.getElementById('v').textContent=D.values[i];
 g.clearRect(0,0,c.width,c.height);g.font='16px system-ui';g.fillStyle='#52606d';g.strokeStyle='#e4e7eb';
 g.textAlign="right";for(const v of nice(y0,y1,6)){{g.beginPath();g.moveTo(L,Y(v));g.lineTo(L+W,Y(v));g.stroke();g.fillText(v,L-8,Y(v)+4)}}g.textAlign="center";
 for(const v of nice(x0,x1,8)){{g.fillText(v,X(v),T+H+20)}}
 g.fillText(D.xlabel,L+W/2,c.height-8);g.save();g.translate(16,T+H/2);g.rotate(-Math.PI/2);g.fillText(D.ylabel,0,0);g.restore();g.textAlign="left";
 let k=0;for(const name in D.series){{const arr=D.series[name][i];g.strokeStyle=D.colors[k%D.colors.length];g.lineWidth=2.4;g.beginPath();
  let pen=false;arr.forEach((v,j)=>{{if(v===null){{pen=false;return}}if(!pen){{g.moveTo(X(D.x[j]),Y(v));pen=true}}else g.lineTo(X(D.x[j]),Y(v))}});g.stroke();k++}}
}}
document.getElementById('lg').innerHTML=Object.keys(D.series).map((n,k)=>`<span><i style="background:${{D.colors[k%D.colors.length]}}"></i>${{n}}</span>`).join('');
s.addEventListener('input',draw);draw();
</script></body></html>"""


def slider_page(path: str | Path, title: str, slider_label: str, slider_values: Sequence,
                x: Sequence[float], series: dict[str, Sequence[Sequence[float]]],
                xlabel: str, ylabel: str, note: str = "", ylim: tuple[float, float] | None = None,
                start: int = 0) -> Path:
    """Write a self-contained HTML page. series[name][i] is the curve for slider_values[i]."""
    for name, curves in series.items():
        if len(curves) != len(slider_values):
            raise ValueError(f"series '{name}' needs one curve per slider value")
    def clean(seq):
        return [None if v != v else float(v) for v in seq]  # NaN -> gap in the line
    data = {"values": [str(v) for v in slider_values], "x": clean(x),
            "series": {k: [clean(c) for c in v] for k, v in series.items()},
            "xlabel": xlabel, "ylabel": ylabel, "ylim": list(ylim) if ylim else None,
            "colors": SERIES + [COLORS["ink"]]}
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_PAGE.format(title=title, note=note, slider_label=slider_label, last=len(slider_values) - 1,
                                 start=start, data=json.dumps(data)), encoding="utf-8")
    print(f"saved explorer: {path}  (open it in a browser and drag the slider)")
    return path

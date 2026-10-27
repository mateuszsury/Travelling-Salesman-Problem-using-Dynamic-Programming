"""Draw the solver result for the matrix used in test_tsp.py; pip install numpy matplotlib."""
import json
from pathlib import Path
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from tsp_python import tsp_dynamic_programming
matrix = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
cost, route = tsp_dynamic_programming(matrix)
assert cost == 80 and route[0] == route[-1] and set(route[:-1]) == set(range(4))
dest = Path(__file__).resolve().parent
(dest / "tour-example.json").write_text(json.dumps({"matrix":matrix,"cost":cost,"route":route}, indent=2)+"\n")
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":12,"svg.hashsalt":"tour-example"})
fig, axes = plt.subplots(1,2, figsize=(10,4.8), layout="constrained", gridspec_kw={"width_ratios":[1,1.4]})
axes[0].imshow(matrix, cmap="Blues")
for i in range(4):
    for j in range(4): axes[0].text(j,i,str(matrix[i][j]),ha="center",va="center",color="white" if matrix[i][j]>20 else "#0f172a")
axes[0].set(xticks=range(4),yticks=range(4),xlabel="To city",ylabel="From city",title="Published cost matrix")
coords=[(0,1),(1.3,1), (1.3,0),(0,0)]
ax=axes[1]
for a,b in zip(route,route[1:]):
    x,y=coords[a]; u,v=coords[b]
    ax.annotate("",xy=(u,v),xytext=(x,y),arrowprops={"arrowstyle":"->","color":"#0284c7","lw":2,"shrinkA":20,"shrinkB":20})
    ax.text((x+u)/2,(y+v)/2,str(matrix[a][b]),ha="center",va="center",bbox={"facecolor":"white","edgecolor":"none","pad":3})
for i,(x,y) in enumerate(coords):
    ax.scatter([x],[y],s=650,color="#0f172a",zorder=3)
    ax.text(x,y,str(i),ha="center",va="center",color="white",zorder=4)
ax.set(xlim=(-.4,1.7),ylim=(-.4,1.4),title="Computed closed tour: total cost 80")
ax.axis("off")
fig.suptitle("Held–Karp example • layout is schematic, edge weights come from the matrix",fontsize=12)
fig.savefig(dest / "tour-example.svg", metadata={"Date":None})

# Normalize generated XML whitespace for clean source diffs.
svg = dest / 'tour-example.svg'
svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")

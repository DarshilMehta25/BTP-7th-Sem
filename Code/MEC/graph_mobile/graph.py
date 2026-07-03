import matplotlib.pyplot as plt
from MEC import DMUA

utility,offloaders_handoff=DMUA.xyz()

print(utility)
print(offloaders_handoff)

x1 = list(range(0,101,10))
y1 = utility
y2 = offloaders_handoff

print(y1)
print(y2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# ── Graph 1: Utility vs Number of Devices ────────────────────────────────────
ax1.plot(x1, y1, marker='o', color='royalblue', linewidth=2, markersize=6)
ax1.set_title('Server Utility vs Number of Devices')
ax1.set_xlabel('Number of Mobile/Moving Devices')
ax1.set_ylabel('Server Utility')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

# ── Graph 2: Handoffs vs Number of Devices ───────────────────────────────────
ax2.plot(x1, y2, marker='s', color='tomato', linewidth=2, markersize=6)
ax2.set_title('Handoffs vs Number of Devices')
ax2.set_xlabel('Number of Mobile/Moving Devices')
ax2.set_ylabel('Number of Handoffs')
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('../Results/MUA_Graphs.png', dpi=150)
# plt.show()
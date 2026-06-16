import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Algos.ServerRA_i import SRA_i
from Algos.SingletonUM import SUM
from Algos.ServerRA import SRA


x_values = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
y_values = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

# plt.plot(x_values, y_values)
# plt.savefig("graph.png")



from Algos import test2, MUMS
from Algos import MUMS
no_of_offloaders=test2.EDs
models=test2.models


#Number of Offloaders vs Max Total Utility
x_values1 = []
y_values1 = []
y_values2 = []
y_values3 = []
successful_offloaders_mums = []
successful_offloaders_sra = []
successful_offloaders_sum = []

time_of_MUMS_execution=[]
time_of_SRA_execution=[]
time_of_SUM_execution=[]



# for i in range(2, len(no_of_offloaders) + 1, 2):
#
#     curr_EDs = no_of_offloaders[:4]
#     X, NxO, UxNxO = MUMS.MUMS(curr_EDs, models, 20e6, 800e9, 2000)
#
#     print("Utility:", UxNxO)
#     x_values1.append(i)
#     y_values1.append(UxNxO)

import copy

import copy
import time


for i in range(2, len(no_of_offloaders) + 1, 2):
    curr_EDs = copy.deepcopy(no_of_offloaders[:i])
    curr_models = copy.deepcopy(models)


    start1=time.time()
    X, Nx01, UxNxO_mums=MUMS.MUMS(curr_EDs,curr_models,20e6,800e9,2000)
    finish1=time.time()

    start2 = time.time()
    UxNoX_sra, Wi_list, Fi_list, Nx02=SRA(curr_EDs,20e6,800e9)
    finish2 = time.time()

    start3=time.time()
    UxSUM, Nx03=SUM(curr_EDs,20e6,800e9)
    finish3=time.time()

    # print(f"{i} EDs -> Utility: {UxNxO}")
    x_values1.append(i)
    y_values1.append(UxNxO_mums) #utility from MUMS
    y_values2.append(UxNoX_sra) #utility from SRA
    y_values3.append(UxSUM) #utility from SUM
    time_of_MUMS_execution.append(finish1-start1)
    time_of_SRA_execution.append(finish2-start2)
    time_of_SUM_execution.append(finish3-start3)
    successful_offloaders_mums.append(len(Nx01))
    successful_offloaders_sra.append(Nx02)
    successful_offloaders_sum.append(len(Nx03))

fig, axs = plt.subplots(3, 1, figsize=(8, 12))

# MUMS
axs[0].plot(x_values1, y_values1)
axs[0].set_title("Dis CNN")
axs[0].set_xlabel("Number of EDs")
axs[0].set_ylabel("Max Total Utility")
axs[0].set_xticks(x_values1)

# SRA
axs[1].plot(x_values1, y_values2)
axs[1].set_title("SRA")
axs[1].set_xlabel("Number of EDs")
axs[1].set_ylabel("Max Total Utility")
axs[1].set_xticks(x_values1)

# SUM
axs[2].plot(x_values1, y_values3)
axs[2].set_title("SUM")
axs[2].set_xlabel("Number of EDs")
axs[2].set_ylabel("Max Total Utility")
axs[2].set_xticks(x_values1)

plt.tight_layout()
plt.savefig("no_of_EDs_vs_max_total_utility.png")

"""

Issue: MUMS() was modifying the original EDs or models objects. Since Python passes objects by reference, changes made in the first call remained for later calls.

So:

MUMS(first 2 EDs)  # modifies objects
MUMS(first 4 EDs)  # uses already modified objects → utility becomes 0

How deepcopy fixed it:

curr_EDs = copy.deepcopy(no_of_offloaders[:i])
curr_models = copy.deepcopy(models)

deepcopy creates completely new independent objects, so each call to MUMS() starts with fresh data and cannot affect later calls.

"""



# print("x =", x_values1)
# print("y =", y_values1)

# print(*x_values1)
# print(*y_values1)

# plt.plot(x_values1, y_values1)
# plt.xlabel("Number of Offloaders")
# plt.ylabel("Max Total Utility")
# plt.title("Number of Offloaders vs Max Total Utility")
# plt.savefig("no_of_offloadersVSmax_total_utility.png")



#Number of offloaders vs Total Energy Consumption





#Number of Offloaders vs Successful Offloaders
fig, axs = plt.subplots(3, 1, figsize=(8, 12))

# MUMS
axs[0].plot(x_values1, successful_offloaders_mums)
axs[0].set_title("MUMS")
axs[0].set_xlabel("Number of EDs")
axs[0].set_ylabel("Successful Offloaders")
axs[0].set_xticks(x_values1)
axs[0].grid(True)

# SRA
axs[1].plot(x_values1, successful_offloaders_sra)
axs[1].set_title("SRA")
axs[1].set_xlabel("Number of EDs")
axs[1].set_ylabel("Successful Offloaders")
axs[1].set_xticks(x_values1)
axs[1].grid(True)

# SUM
axs[2].plot(x_values1, successful_offloaders_sum)
axs[2].set_title("SUM")
axs[2].set_xlabel("Number of EDs")
axs[2].set_ylabel("Successful Offloaders")
axs[2].set_xticks(x_values1)
axs[2].grid(True)

plt.tight_layout()
plt.savefig("successful_offloaders.png", dpi=300)


# for i in successful_offloaders:
#     print(len(i))
#Number of Offloaders vs Average Inference Delay



#Number of Offloaders vs Average Execution Time

fig, axs = plt.subplots(3, 1, figsize=(8, 12))

# MUMS
axs[0].plot(x_values1, time_of_MUMS_execution,
            marker='o')
axs[0].set_title("MUMS")
axs[0].set_xlabel("Number of Offloaders")
axs[0].set_ylabel("Average Execution Time (s)")
axs[0].set_xticks(x_values1)
axs[0].grid(True)

# SRA
axs[1].plot(x_values1, time_of_SRA_execution,
            marker='s')
axs[1].set_title("SRA")
axs[1].set_xlabel("Number of Offloaders")
axs[1].set_ylabel("Average Execution Time (s)")
axs[1].set_xticks(x_values1)
axs[1].grid(True)

# SUM
axs[2].plot(x_values1, time_of_SUM_execution,
            marker='^')
axs[2].set_title("SUM")
axs[2].set_xlabel("Number of Offloaders")
axs[2].set_ylabel("Average Execution Time (s)")
axs[2].set_xticks(x_values1)
axs[2].grid(True)

plt.tight_layout()
plt.savefig("no_of_offloadersVSavg_execution_time.png", dpi=300)
plt.close()
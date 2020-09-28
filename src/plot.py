import matplotlib.pyplot as plt
import csv

with open("data.csv", newline='') as csvfile:
    data = list(csv.reader(csvfile))

n_nodes = []
transactions = []
time = []
transaction_sec = []

for i in range(len(data)):
    n_nodes.append(float(data[i][0]))
    transactions.append(float(data[i][1]))
    time.append(float(data[i][2]))
    transaction_sec.append(float(data[i][3]))

fig, ax = plt.subplots()
ax.plot(n_nodes, transaction_sec)

ax.set(xlabel='nodes (n)', ylabel='transactions per second (t/s)',
       title="Network throughput")


fig.savefig("test.pdf", format="pdf")
plt.show()

import tkinter
import matplotlib.pyplot as plt
from collections import Counter

db=DBHelper()
db.connection()
answer=db.fetch("select distinct(source) from flight")
answer2=db.fetch("select source from flight")
#print(answer)


sources = []
sources2 = []
numberfl=[]


for i in answer:
    sources.append(i['source'])

for i in answer2:
    sources2.append(i['source'])
print(sources)

print(sources2)
count=Counter(sources2)

print(count)
numberfl=list(count.values())
print(numberfl)

plt.bar(sources,numberfl)
plt.ylim(0, 10)
plt.xlabel("City")
plt.ylabel("Number of flights")
plt.title("Flight analysis")
plt.show()
print("Source = ",sources)

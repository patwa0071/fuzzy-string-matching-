import math
import operator
import matplotlib.pyplot as plt
# The longest common subsequence in Python


# Function to find lcs
def lcs(S1, S2, m, n,ratio_calc=False):
    L = [[0 for x in range(n+1)] for x in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif S1[i-1] == S2[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    index = L[m][n]
    if ratio_calc == True:
        # Computation of the lcs Ratio
        Ratio = (index / math.sqrt(len(S1)*len(S2)))
        return Ratio
    else:
        # This is the length of lcs
        return (index)
        
q_str=input("Enter the query word: \n")
threshold=float(input("Enter threshold value: \n"))
threshold=threshold/100
data=open('data.txt',"r")
text=data.read()
text=text.lower().split('\n')
lis=[]
for row in text:
    temp=lcs(q_str, row,len(q_str),len(row))
    Ratios=lcs(q_str, row,len(q_str),len(row), True) 
    lis.append([row,temp,Ratios]) 
lis.sort(key=operator.itemgetter(2,1))
lis.reverse()
print("\nBest Found Matches: ")
for record in lis:
     if record[2]>=threshold:
        print(record)
        plt.stem(record[2],record[0])
plt.show()

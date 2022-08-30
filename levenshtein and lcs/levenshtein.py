import numpy as np
import operator
import matplotlib.pyplot as plt
def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for row in range(1, rows):
        for col in range(1, cols):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # This is the minimum number of edits needed to convert string a to string b
        return (distance[row][col])

q_str=input("Enter the query word: \n")
threshold=float(input("Enter threshold value: \n"))
threshold=threshold/100
data=open('data.txt',"r")
text=data.read()
text=text.lower().split('\n')
lis=[]
for row in text:
    temp=levenshtein_ratio_and_distance(q_str, row)
    Ratios=levenshtein_ratio_and_distance(q_str, row, True) 
    lis.append([row,temp,Ratios])
lis.sort(key=operator.itemgetter(2,1))
lis.reverse()
print ("\nBest Found Matches: ")
for record in lis:
    if record[2]>=threshold:
        print(record)
        plt.stem(record[2],record[0])
plt.show()



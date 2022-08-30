
import matplotlib.pyplot as plt
import operator
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
stop_words= set(stopwords.words('english')) #for removing stopwords.
string = input("\nEnter string: \n")
input_word_tokens=word_tokenize(string)
filtered_sentence = [w for w in input_word_tokens if not w.lower() in stop_words]
filtered_sentence=[]
for w in input_word_tokens:
	if w not in stop_words:
		filtered_sentence.append(w)
sortedMatches = []

#This function accepts two lists as parameters and returns the jaccard index.
def jaccardIndex(x,y):
	intersection = len(list(set(x).intersection((set(y)))))
	union = len(list(set(x).union((set(y)))))
	return intersection/union

data = open('d.txt','r')
text=data.read() 
text=text.lower().split('\n')


lis=[]
 

for row in text:
	word_tokens=word_tokenize(row)
	filtered=[w for w in word_tokens if not w.lower() in stop_words]
	filtered=[]
	for w in word_tokens:
		if w not in stop_words:
			filtered.append(w)
	si = jaccardIndex(filtered_sentence,filtered)
	lis.append([row,si])
lis.sort(key=operator.itemgetter(1)) #Sort the records based on jaccard index and text

#descending order:
lis.reverse()
# print(lis)
threshold=float(input("\nenter threshold value : \n"))
threshold=threshold/100

#matching data found based on a threshold
print("\nBest Found Matches: \n ")
for record in lis:
	if record[1]>=threshold:
		print(record)
		print()
		plt.stem(record[1],record[0])
plt.show()
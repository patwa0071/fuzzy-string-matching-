import math
import matplotlib.pyplot as plt
import operator
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords') #for removing stopwords.

def read_and_get_data(filename):
    sentence_list=[]
    fr = open(filename, 'r')
    text = fr.read()
    fr.close()
    text = text.lower().split('\n')
    list_of_word_list = []
    for each_sentence in text:
        sentence_list.append(each_sentence)
    for each_sentence in sentence_list:
        word_list = []
        for each_word in each_sentence.split():
            if each_word not in stopwords.words():
                word_list.append(each_word)
        list_of_word_list.append(word_list)
    print(list_of_word_list)
    return list_of_word_list

#word_freq = no. of times a word in appears in a sentence 

def calculate_word_freq(clean_word_list):
    word_freq = {}
    for each_word in clean_word_list:
        if each_word in word_freq:
            word_freq[each_word] += 1
        else:
            word_freq[each_word] = 1
    return word_freq

# tf = no of times a word appears in a sentence / total no of words in that sentence

def compute_tf(word_freq, clean_word_list):
    word_tf = {}
    for word, count in word_freq.items():
        temp = len(clean_word_list)
        word_tf[word] = count/float(temp)
    return word_tf

# idf = log( no of sentences / no of sentences containing the word w )

def compute_idf(doc_list,temp):
    word_idf = {}
    no_of_docs = len(doc_list)

    for each_word in temp:
        no_docs_with_it=0
        for each_doc in doc_list:
            if each_word in each_doc.keys():
                no_docs_with_it+=1
        word_idf[each_word]=math.log(no_of_docs/float(no_docs_with_it))
    return word_idf

# tfidf = tf * idf

def compute_tfidf(tf, idf):
    
    list_of_tfidf_in_each_sentence=[]
    for each_dic_of_tf in tf:
        tfidf_in_each_sentence = {}
        for word,val in each_dic_of_tf.items():
            tfidf_in_each_sentence[word] = val*idf[word]
        list_of_tfidf_in_each_sentence.append(tfidf_in_each_sentence)
    return list_of_tfidf_in_each_sentence

def cosine_similarity(tfidf):
    fr=open('d.txt',"r")
    data=fr.read()
    data=data.lower().split('\n')
    fr.close()
    list_cosine_similarity=[]
    sum2=0
    for word,val in tfidf[len(tfidf)-1].items():
        sum2+=val*val
    
    for tfidf_each_sentence in tfidf:
        dot_prod=float(0)
        for word,val in tfidf[len(tfidf)-1].items():
            if word not in tfidf_each_sentence.keys():
                pass
            else:
                dot_prod+=tfidf_each_sentence[word]*val
        sum1=0
        for word,val in tfidf_each_sentence.items():
            sum1+=val*val
        sum3=0
        sum3=math.sqrt(sum1) * math.sqrt(sum2)
        list_cosine_similarity.append(dot_prod/sum3)
    lis=[]
    for i in range(len(list_cosine_similarity)):
        lis.append([data[i],list_cosine_similarity[i]])
    return lis

def recommend(list_cosine_similarity,filename,threshold):
    cs={}
    fr=open(filename,"r")
    text=fr.read()
    fr.close()
    text=text.lower().split('\n')
    i=0
    for each_sentence in text:
        cs[each_sentence]=list_cosine_similarity[i][1]
        i+=1
    threshold=(threshold/100)
    answer=[]
    for each_sentence,val in cs.items():
        if(val>=threshold):
            answer.append([each_sentence,val])
    answer.sort(key=operator.itemgetter(1))
    answer.reverse()
    for data in answer:
        print(data)
        print()
        plt.stem(data[1],data[0])
    plt.show()
str=input("\n Enter string: \n")
print()
threshold=float(input("Enter threshold value: \n"))
print()
open_file=open('d.txt', "a")
open_file.write("\n")
open_file.write(str)
open_file.close()
list_of_word_list=read_and_get_data('d.txt')
# print(" ======== Calculating word freq in each sentence ========== ")
list_of_word_freq_in_each_sentence=[]
tf=[]
for each_list in list_of_word_list:
    word_freq_in_each_sentence={}
    word_freq_in_each_sentence=calculate_word_freq(each_list)
    tf.append(compute_tf(word_freq_in_each_sentence,each_list))
    list_of_word_freq_in_each_sentence.append(word_freq_in_each_sentence)
# print(list_of_word_freq_in_each_sentence)
# print('\n')
# print(" ======== Calculating tf in each sentence ========== ")
# print(tf)
# print(" ======== Calculating idf of each word in the whole dataset ========== ")
temp=set()
for each_dic in list_of_word_freq_in_each_sentence:
    for each_key in each_dic.keys():
        temp.add(each_key)
idf = compute_idf(list_of_word_freq_in_each_sentence,temp)
# print("idf")
# print(idf)
# print('\n')
# print(" ======== Calculating tfidf in each sentence ========== ")
tfidf = compute_tfidf(tf, idf)
# print(tfidf)
# print('\n')
# print(" ======== cosine_similarity ======== ")
list_cosine_similarity=(cosine_similarity(tfidf))
# print(list_cosine_similarity)
fd=open("d.txt","r")
d=fd.read()
fd.close()
m=d.split("\n")
s="\n".join(m[:-1])
fd=open("d.txt","w+")
for i in range(len(s)):
    fd.write(s[i])
fd.close()
print("\nBest Found Matches: \n")
recommend(list_cosine_similarity,'d.txt',threshold)


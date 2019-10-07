import sys,csv

with open('../in/Entries .csv', 'r') as f:
  reader = csv.reader(f)
  words_list = list(reader)
f.close()

#ignore unnecessary parts
words_list_ignored=[]
for i in words_list:
  words_list_ignored.append(i[0:2])

words_list=words_list_ignored

def remove_duplicates(l):
    return list(set(l))

english=[]
for i in words_list:
  english.append(i[0])

english_no_duplicate=remove_duplicates(english)

dictionary_en_to_fa=dict()

for i in english_no_duplicate:
  dictionary_en_to_fa[i]=""

for i in words_list:
  dictionary_en_to_fa[i[0]]=i[1]


final_list_english=[]
def dictionaryContains(word):
    if word in dictionary_en_to_fa :
        return True
    else :
        return False  

def wordBreakUtil(string, n, result):
    for i in range(1,n+1):
        prefix=string[0:i]
        if dictionaryContains(prefix):
            if i == n :
                result += prefix
                final_list_english.append(result)
                return
            wordBreakUtil(string[i : ], n-i, result + prefix + " ")  


f2 = open('../in/in_2.txt', "r")

input_sentence=f2.readline()
f2.close()
splitted_raw_list=input_sentence.split()
string=""
for i in range(len(splitted_raw_list)):
    for j in words_list:    
        if splitted_raw_list[i] == j[1]:
            string+=j[0]
            break

wordBreakUtil(string,len(string),"")

final_list_persian=[]

for line_e in final_list_english:
  line_list_f=[]
  line_list_e=line_e.split()
  for word_e in line_list_e:
    word_f=dictionary_en_to_fa[word_e]
    line_list_f.append(word_f)
  final_list_persian.append(line_list_f) 

final_persian_string=[]
for line in final_list_persian:
  temp_line=""
  for word in line:
    temp_line+=word+"-"
  final_persian_string.append(temp_line[:-1])  

f3 = open("../out/out.txt", "w")

last=len(final_persian_string)
first=0
for i in final_persian_string:
  first+=1
  print(i)
  f3.write(i)
  if(last != first):
    f3.write("\n")
f3.close()
import sys
import gzip
import string
import re
import queue
import matplotlib.pyplot as plt


# Your function start here
def fancy(list,queue1):
    

        token = queue1.get()
        list.append(token)
        queue1.put(token)

        while(queue1.empty() == False):
            token = queue1.get()
            
            if(token.isspace()):
                continue
            if(token in string.punctuation):
                continue

            
            
        
         # URL- 2
            if(token.startswith("https://") | token.startswith("http://")):
                while(token[-1] in string.punctuation):
                    token = token[:-1]
                list.append(token)
                continue

         # Lowercase - 3
            token = token.lower()
            

            

         # Numbers as single token - 4
            isNumber = 1
            for char in token:
                if(char.isalpha()==True):
                    isNumber = 0
                elif(char in string.punctuation):
                    if(char not in [',' , '-' , '+' , '.']):
                        isNumber = 0

            if(isNumber == 1):
                list.append(token)
                continue



         # Apostrophes - 5
            tempList = ''
            for char in token:
                if(char == "'"):
                    continue
                else:
                    tempList=tempList + char
            token = tempList
            
           

         # Abbreviations - 6
            isAbv = 1
            if(token.isalnum()):
                isAbv=0
            for char in token:
                if(char in string.punctuation):
                    if(char != '.'):
                        isAbv=0

            if(isAbv==1):
                tempList = ''
                for char in token:
                    if(char == "."):
                        continue
                    else:
                        tempList=tempList + char
                token = tempList
                

            

         # Hyphens - 7
            isHyphen=0
            for char in token:
                if(char == '-'):
                    isHyphen = 1

            if(isHyphen == 1):
                split = token.split('-')
                tempList = ''
                for char in token:
                    if(char == "-"):
                        continue
                    else:
                        tempList=tempList + char
            
                for token in split:
                    queue1.put(token)
                queue1.put(tempList)
                continue

           

         # Remove punctuation - 8
           
            isPunc=1
            if(token.isalnum()):
                isPunc=0

            for char in token:
                if(char in string.punctuation):
                    if((char == '.') & (char == '-')):
                        isPunc=0
            

            if(isPunc==1):
                pattern = r'[^a-zA-Z0-9.-]+'
                isRemoved=0
                result = re.split(pattern, token)
                if(len(result)>1):
                    isRemoved=1
            
            
                result = [token for token in result if token]

                if(isRemoved==1):
                    # print(result)
                    for tok in result:
                        queue1.put(tok)
                    continue
            

            list.append(token)
           
                
        return list

def checkShort(str):
    vowels=['a','e','i','o','u','y']
    if((str[0] in vowels) & (str[1] not in vowels) & (len(str)<3)):
        # print(str)
        return True

    if((str[-1]!='w') & (str[-1]!='x')):
        if(str[-2] in vowels):
            for char in str[:-3]:
                if char in vowels:
                    return False
            return True
    return False

def stemToken(str):
    vowels=['a','e','i','o','u','y']
    step1a = False
    step1b = False
    step1c = False


    # Step - 1A
    if((str.endswith("sses")) & (step1a==False)):
        str = str[:-2]
        step1a=True

    if( (((str.endswith("ied")) | (str.endswith("ies"))) & (step1a==False))):
        str = str[:-3]
        if( len(str) > 1):
            str=str+'i'
        else:
            str=str+'ie'
        step1a=True
    
    if( (str.endswith("ss")) | (str.endswith("us")) & (step1a==False)):
        step1a=True

    if((str.endswith("s")) & (step1a==False)):
        for char in str[:-2]:
            if(char in vowels):
                str=str[:-1]
                break
        step1a=True

    # Step - 1B
    if( (str.endswith("eed")) | (str.endswith("eedly")) & (step1b==False)):
        temp=str
        flag=0
        if(temp.endswith("eed")):
            temp=temp[:-3]
        else:
            temp=temp[:-5]
        if(len(temp)>1):
            if( (temp[-1] not in vowels) & (temp[-2] in vowels) ):
                flag=1
                temp = temp+'ee'
        if(flag==1):
            str = temp
            step1b=True

    if( ((str.endswith("ed")) | str.endswith("edly") | (str.endswith("ing")) | (str.endswith("ingly")) & (step1b==False)) ):
        
        list = ["bb", "dd", "ff", "gg", "mm", "nn", "pp", "rr","tt"]
        temp=str
        flag=0
        if(str.endswith("ed")):
            temp=temp[:-2]
        elif(str.endswith("edly")):
            temp=temp[:-4]
        elif(str.endswith("ing")):
            temp=temp[:-3]
        else:
            temp=temp[:-5]
        for char in temp:
            if(char in vowels):
                flag=1
                str=temp
                # print(str)
                break
        
        if(flag==0):
            step1b=True
        
        elif(flag == 1):
            if( (str.endswith("at") | str.endswith("bl") | str.endswith("iz"))  & (step1b==False) ):
                str=str+'e'
                step1b=True
            
            last2=str[-1]+str[-2]
            if((last2 in list) & (step1b==False)):
                str=str[:-1]
                step1b=True

            if(checkShort(str) & (step1b==False)):
                # print(str)
                str=str+'e'
                step1b=True

    #Step 1c
    if(len(str)>2):
        if((str.endswith('y')) & (str[-2] not in vowels) & (len(str) > 2 )):
            str=str[:-1]
            str=str + 'i'

    return str

   
def textFileProcess(inputFile, outputFilePrefix,tokenize_type,stoplist_type,stemming_type):
    tokensList=[]
    try:
        with gzip.open(inputFile, 'rt') as infile:
            file_contents = infile.read()
            tokens = file_contents.split()

            for token in tokens:
                tokensList.append([token])


    
    except FileNotFoundError:
        print("Input file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    # Tokenization
    tokenizeList = []
    if(tokenize_type == "spaces"):
        for tokens in tokensList:
            temp=[]
            for token in tokens:
                temp.append(token)
                temp.append(token)
            tokenizeList.append(temp)

    if(tokenize_type == "fancy"):
        for tokens in tokensList:
            temp=[]
            for token in tokens:
                queue1 = queue.Queue()
                queue1.put(token)
                temp = fancy(temp,queue1)

            tokenizeList.append(temp)

    # Stopping
    stopList = []
    
    if(stoplist_type =="noStop"):
        stopList=tokenizeList

    elif(stoplist_type =="yesStop"):
        for tokens in tokenizeList:
            temp=[]
            temp.append(tokens[0])
            for token in tokens[1:]:
                if(token in stopword_lst):
                    continue
                else:
                    temp.append(token)


            stopList.append(temp)

    # Stemming 
    stemList=[]

    if(stemming_type == "noStem"):
        stemList = stopList
    
    elif(stemming_type == "porterStem"):
        for tokens in stopList:
            temp=[]
            temp.append(tokens[0])
            for token in tokens[1:]:
                stemmedToken = stemToken(token)
                temp.append(stemmedToken)
            
            stemList.append(temp)


    num_tokens = 0
    unique_tokens = set()
    token_counts = {}
    collWords=[0]
    vocabWords=[0]
    try:
         with open(outputFilePrefix +'-tokens'+'.txt', 'w') as outfile:
            for token in stemList:  
                for tokens in token:
                    outfile.write(f"{tokens} ")
                outfile.write(f"\n")

         
         with open(outputFilePrefix +'-heaps'+'.txt', 'w') as outfile:
            for token in stemList:  
                for tokens in token[1:]:
                    num_tokens+=1
                    if(tokens not in unique_tokens ):
                        unique_tokens.add(tokens)
                    if((num_tokens%10)==0):
                        outfile.write(f"{num_tokens} {len(unique_tokens)}\n")
            outfile.write(f"{num_tokens} {len(unique_tokens)}\n")

         with open(outputFilePrefix +'-stats'+'.txt', 'w') as outfile:
            for token in stemList:  
                for tokens in token[1:]:
                    token_counts[tokens] = token_counts.get(tokens, 0) + 1
            outfile.write(f"{num_tokens}\n")
            outfile.write(f"{len(unique_tokens)}\n")
            sorted_tokens = sorted(token_counts.items(), key=lambda x: (-x[1], x[0]))
            for i, (token, count) in enumerate(sorted_tokens[:100], start=1):
                outfile.write(f"{token} {count}\n")

         with open(outputFilePrefix +'-heaps'+'.txt', 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    collWords.append(int(parts[0]))
                    vocabWords.append(int(parts[1]))

             
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # print(collWords[1],vocabWords[1])


   

    plt.figure(figsize=(12, 8))
    plt.plot(collWords, vocabWords, marker='.', linestyle='-', color='k',linewidth=-1)
    plt.title("Vocabulary Growth for Sense and Sensibility")
    plt.xlabel("Words in Collection")
    plt.ylabel("Words in Vocabulary")
    plt.xlim(0)
    plt.ylim(0)
    plt.grid(True)
    plt.show() 

    


if __name__ == '__main__':
    # Read arguments from command line; or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else "P1-train.gz"
    outputFilePrefix = sys.argv[2] if argv_len >= 3 else "outPrefix"
    tokenize_type = sys.argv[3] if argv_len >= 4 else "spaces"
    stoplist_type = sys.argv[4] if argv_len >= 5 else "yesStop"
    stemming_type = sys.argv[5] if argv_len >= 6 else "porterStem"

    # Below is stopword list
    stopword_lst = stopword_lst = ["a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
                    "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to",
                    "was", "were", "with"]

    textFileProcess(inputFile, outputFilePrefix,tokenize_type,stoplist_type,stemming_type)
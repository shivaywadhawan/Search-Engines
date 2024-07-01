# import package ...
import sys
import gzip
import json
from collections import defaultdict
import math


def buildIndex(inputFile):
    # Your function start here ...
    inverted_index = defaultdict(list)
    term_counts = defaultdict(int)
    doc_lengths = defaultdict(int)
    docID2storyID = {}

    try:
        with gzip.open(inputFile, 'rb') as f:
            data = json.load(f)
            # print(data.keys())

        doc_id = 1
        for document in data['corpus']:
            storyID = document['storyID']
            text = document['text']
            docID2storyID[doc_id] = storyID
            # if(storyID=="38482-art38"):
            #     print(text)
          

            tokens = text.split()

            for position, token in enumerate(tokens):
                
                inverted_index[token].append((doc_id, position)) 
                
                term_counts[token] += 1
                doc_lengths[doc_id] += 1
                
                # print(inverted_index)

            doc_id += 1

    except Exception as e:
         print(f"An error occurred: {e}")
         return None

    return inverted_index, term_counts, doc_lengths, docID2storyID




def runQueries(index, queriesFile, outputFile):
    try:
        with open(queriesFile, 'r') as f:
            queries = f.readlines()
    

        with open(outputFile, 'w') as f_out:
            for query in queries:
                query = query.strip().split('\t')
                tempQuesry=[]
                if(len(query)==1):
                    tempQuesry = query[0].split()
                    query=tempQuesry
                
                query_type = query[0].lower() 
                query_name = query[1]
                query_terms = query[2:]
            

                if query_type == 'and':
                    matching_docs = []

                    for term in query_terms:
                        if term in index[0]:  
                            postings = index[0][term] 
                            matching_docs.append(set([posting[0] for posting in postings]))

                    # print(matching_docs)

                    if matching_docs:
                        and_result = set.intersection(*matching_docs)
                        and_result2={}
                        for i in and_result:
                            and_result2[i]=index[3][i]

                        
                        and_result2 = dict(sorted(and_result2.items(), key=lambda item: item[1]))
                       
                        for rank, doc_id in enumerate(and_result2, start=1):
                            f_out.write(f"{query_name:<10} skip  {index[3][doc_id]:<20}{rank:<5}1.0000  swadhawan\n")

                elif query_type == 'or':
                        matching_docs = set()
                        for term in query_terms:
                            if term in index[0]:
                                for doc_id, _ in index[0][term]:
                                    matching_docs.add(doc_id)
                        
                        for rank, doc_id in enumerate(matching_docs, start=1):
                            f_out.write(f"{query_name:<10} skip  {index[3][doc_id]:<20}{rank:<5}1.0000  swadhawan\n")

                elif query_type == 'ql':
                        mu=300
                        collection_length = sum(index[1].values())
                        ql_scores = defaultdict(float)
                        matching_docs = set() 
                        for term in query_terms:
                            if term in index[0]:
                                for doc_id, _ in index[0][term]:
                                    matching_docs.add(doc_id)

                        for doc_id in matching_docs:
                            doc_score = 0.0
                            lambda_value = float(mu / (index[2][doc_id] + mu))
                            doc_terms = set(index[0].keys())
                            query_set = set(query_terms)
                            common_terms = doc_terms.intersection(query_set)
                            if common_terms:
                                for term in query_terms:
                                    term_freq_in_doc = sum(1 for doc, _ in index[0][term] if doc == doc_id)
                                    collection_freq = index[1][term]
                                    smoothed_prob = (1 - lambda_value) * (term_freq_in_doc / index[2][doc_id])
                                    smoothed_prob += lambda_value * (collection_freq / collection_length)
                                    if smoothed_prob > 0:
                                        doc_score += math.log(smoothed_prob)
                                ql_scores[doc_id] = doc_score
                        sorted_docs = sorted(ql_scores.items(), key=lambda x: x[1], reverse=True)
                        for rank, (doc_id,score) in enumerate(sorted_docs, start=1):
                            f_out.write(f"{query_name:<10} skip  {index[3][doc_id]:<20}{rank:<5}{score:.4f}  swadhawan\n")

                elif query_type == 'bm25':        
                    k1 = 1.8
                    k2 = 5
                    b = 0.75
                    matching_docs = set()  
                    top_documents = []
                    for term in query_terms:
                        if term in index[0]:
                            for doc_id, _ in index[0][term]:
                                matching_docs.add(doc_id)

                    avdl = sum(index[2].values()) / len(index[2]) if len(index[2]) > 0 else 0   
                    N = len(index[2])  
                    bm25_scores = defaultdict(float)
                    

                    for doc_id in matching_docs:
                        doc_score = 0.0
                        dl = index[2][doc_id] 
                        K = k1 * ((1 - b) + (b * (dl / avdl)))  
                        for term in query_terms:
                            temp=[]
                            for i,pos in index[0][term]:
                                if i not in temp:
                                    temp.append(i)
                            ni=len(temp)
                            fi = sum(1 for doc, _ in index[0][term] if doc == doc_id)  

                            qfi = query_terms.count(term) 
                            idf = math.log(((N - ni + 0.5) / (ni + 0.5) )) if ((ni + 0.5)>0) & ((N - ni + 0.5)>0) else 0.0 
                            tf = ((k1 + 1) * fi) / (K + fi) if (K + fi) > 0 else 0.0  
                            qf = ((k2 + 1) * qfi) / (k2 + qfi) if (k2 + qfi) > 0 else 0.0  

                            doc_score += idf * tf * qf  

                        bm25_scores[doc_id] = doc_score

                   
                    sorted_docs = sorted(bm25_scores.items(), key=lambda x: x[1], reverse=True)
                    top_10_docs = sorted_docs[:10]

                    # try:
                    #     with gzip.open(inputFile, 'rb') as f:
                    #         data = json.load(f)
                    
                    #     for doc_id, _ in top_10_docs:
                    #         doc_text = data['corpus'][doc_id-1]['text'] 
                    #         top_documents.append(doc_text)
                    
                    # except Exception as e:
                    #     print(f"An error occurred: {e}") 
                    #     pass
                    
                    for rank, (doc_id, score) in enumerate(sorted_docs, start=1):
                        f_out.write(f"{query_name:<10} skip  {index[3][doc_id]:<20}{rank:<5}{score:.4f}  swadhawan\n")
                    
                    # for i, doc_text in enumerate(top_documents, start=1):
                    #     print(f"Document {i}:\n{doc_text}\n{'=' * 50}\n")



    except Exception as e:
        print(f"An error occurred: {e}") 
        pass
    
    return



if __name__ == '__main__':
    # Read arguments from command line, or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else "sciam.json.gz"
    queriesFile = sys.argv[2] if argv_len >= 3 else "trainQueries.tsv"
    outputFile = sys.argv[3] if argv_len >= 4 else "trainQueries.trecrun"

    index = buildIndex(inputFile)

    if queriesFile == 'showIndex':
        # Invoke your debug function here (Optional)
        pass
    elif queriesFile == 'showTerms':
        # Invoke your debug function here (Optional)
        pass
    else:
        runQueries(index, queriesFile, outputFile)
        # pass

    # Feel free to change anything

# import package ...
import sys
import math
# from prettytable import PrettyTable


def eval(trecrunFile, qrelsFile, outputFile):
    # Your function start here ...
    with open(outputFile, 'w') as output:
        qrelsData = readQrelsFile(qrelsFile)
        trecrunData = readTrecrunFile(trecrunFile)
        totalnumRels=0
        totalrelFound=0
        totalP10=0
        totalR10=0
        totalF1=0
        totalrr=0
        totalap=0
        totalndcg=0

        
        for i in trecrunData:
            numRels=0
            relFound=0
            recall_at_10=0
            cnt=0
            relFoundTen=0
            ap=[]
            rank=0
            
            
            # numRels and numRels
            for j in qrelsData[i]:
                cnt=cnt+1
                if(qrelsData[i][j]!=0 ):
                    numRels = numRels+1
                    if(j in trecrunData[i]):
                        relFound=relFound+1
                        if(relFound==1):
                            rank=cnt

            # NDCG@20
            ndcg20=0
            if(numRels!=0):
                dcg20=0
                x=1
                temp=[]
                for j in range(20):
                    docId = list(trecrunData[i].keys())[j]
                    if(docId in qrelsData[i]):
                        rel = qrelsData[i][docId]
                    else:
                        rel=0
                    if(x !=1):
                        dcg20= dcg20+ rel/math.log2(x)
                    else:
                        dcg20=rel
                    x=x+1

                idcg20=0
                y=1
                for j in range(len(qrelsData[i])):
                    docId = list(qrelsData[i].keys())[j]
                    temp.append(qrelsData[i][docId])
                
                temp.sort(reverse=True)
                for k in temp[0:20]:
                    if(y!=1):
                        idcg20= idcg20+ k/math.log2(y)
                    else:
                        idcg20=k
                    y=y+1
                
                # print(idcg20)
                ndcg20=dcg20/idcg20

            # R@10
            for j in range(10):
                    docId = list(trecrunData[i].keys())[j]
                    if docId in qrelsData[i] and qrelsData[i][docId] != 0:
                        relFoundTen = relFoundTen + 1

            recall_at_10 = relFoundTen / numRels if numRels > 0 else 0


            # P@10
            precision_at_10 = relFoundTen / 10

            # F@10
            f1_at_10 = (2*recall_at_10*precision_at_10)/(precision_at_10+recall_at_10) if (precision_at_10>0) & (recall_at_10>0) else 0

            # AP 
            relFoundAP=0
            for j in range(len(trecrunData[i])):
                docId = list(trecrunData[i].keys())[j]
                j=j+1
                if docId in qrelsData[i] and qrelsData[i][docId] != 0:
                    relFoundAP=relFoundAP+1
                    ap.append(relFoundAP/j)


            avgPrecision = sum(ap)/(numRels) if numRels > 0 else 0

            #reciprocalRank
            for j in range(len(trecrunData[i])):
                    docId = list(trecrunData[i].keys())[j]
                    if docId in qrelsData[i] and qrelsData[i][docId] != 0:
                        rank=j+1
                        break
            if(relFound!=0):
                rr=1/rank
            else:
                rr=0

            output.write(f"NDCG@20      {i:6}  {ndcg20:6.4f}\n")                        
            output.write(f"numRel       {i:6}  {numRels}\n")
            output.write(f"relFound     {i:6}  {relFound}\n")
            output.write(f"RR           {i:6}  {rr:6.4f}\n")
            output.write(f"P@10         {i:6}  {precision_at_10:6.4f}\n")
            output.write(f"R@10         {i:6}  {recall_at_10:6.4f}\n")
            output.write(f"F1@10        {i:6}  {f1_at_10:6.4f}\n")
            output.write(f"AP           {i:6}  {avgPrecision:6.4f}\n")

            totalnumRels=totalnumRels+numRels
            totalrelFound=totalrelFound+relFound
            totalP10=totalP10+precision_at_10
            totalR10=totalR10+recall_at_10
            totalF1=totalF1+f1_at_10
            totalrr=totalrr+rr
            totalap=totalap+avgPrecision
            totalndcg=totalndcg+ndcg20
        
        output.write(f"NDCG@20       all     {(totalndcg/len(trecrunData)):6.4f}\n")
        output.write(f"numRel        all     {totalnumRels}\n")
        output.write(f"relFound      all     {totalrelFound}\n")
        output.write(f"MRR           all     {(totalrr/len(trecrunData)):6.4f}\n")
        output.write(f"P@10          all     {(totalP10/len(trecrunData)):6.4f}\n")
        output.write(f"R@10          all     {(totalR10/len(trecrunData)):6.4f}\n")
        output.write(f"F1@10         all     {(totalF1/len(trecrunData)):6.4f}\n")
        output.write(f"MAP           all     {(totalap/len(trecrunData)):6.4f}\n")
        
            


    return

# Comment out below
query_numbers=['23849', '42255', '47210', '67316', '118440', '121171', '135802', '141630', '156498', '169208', '174463', '258062', '324585', '330975', '332593', '336901', '390360', '405163', '555530', '583468', '640502', '673670', '701453', '730539', '768208', '877809', '911232', '914916', '938400', '940547', '940548', '997622', '1030303', '1037496', '1043135', '1049519', '1051399', '1056416', '1064670', '1071750', '1103153', '1105792', '1106979', '1108651', '1108729', '1109707', '1110678', '1113256', '1115210', '1116380', '1119543', '1121353', '1122767', '1127540', '1131069', '1132532', '1133579', '1136043', '1136047', '1136769', '1136962', 'all']
bm25_ap=['0.0186', '0.2625', '0.2021', '0.0151', '0.0048', '0.6956', '0.1176', '0.4690', '0.0701', '0.1075', '0.0301', '0.0317', '0.0369', '0.2357', '0.2310', '0.0634', '0.2741', '0.0735', '0.0134', '0.7267', '0.0878', '0.0416', '0.5531', '0.1356', '0.2433', '0.2516', '0.1542', '0.2860', '0.1043', '0.0892', '0.0000', '0.0524', '0.5014', '0.3181', '0.1031', '0.0000', '0.0113', '0.0000', '0.2312', '0.2685', '0.0000', '0.3840', '0.5034', '0.0250', '0.0000', '0.1750', '0.3262', '0.4969', '0.0887', '0.0111', '0.0000', '0.2349', '0.3235', '0.2764', '0.0856', '0.1044', '0.6666', '0.1569', '0.0464', '0.0000', '0.4879', '0.1886']
ql_ap=['0.0151', '0.1987', '0.1997', '0.0080', '0.0041', '0.6916', '0.1164', '0.3959', '0.0564', '0.1319', '0.0041', '0.0314', '0.0449', '0.1675', '0.2522', '0.0634', '0.3275', '0.0787', '0.0084', '0.6706', '0.1199', '0.0324', '0.5663', '0.2034', '0.2353', '0.1914', '0.2038', '0.3638', '0.1660', '0.0868', '0.0000', '0.0748', '0.5014', '0.4259', '0.1128', '0.0000', '0.0201', '0.0000', '0.2233', '0.2587', '0.0000', '0.3999', '0.6340', '0.0547', '0.0000', '0.1502', '0.4205', '0.4953', '0.0915', '0.0396', '0.0000', '0.2557', '0.3460', '0.2693', '0.0288', '0.1666', '0.6677', '0.0976', '0.0666', '0.0000', '0.4689', '0.1952']
dpr_ap=['0.2391', '0.4411', '0.3692', '0.0853', '0.0084', '0.2195', '0.0546', '0.4309', '0.1348', '0.1028', '0.1838', '0.1640', '0.3791', '0.5441', '0.2221', '0.1708', '0.2375', '0.0013', '0.2544', '0.7084', '0.1880', '0.0009', '0.3160', '0.1628', '0.0623', '0.2097', '0.1592', '0.4061', '0.3848', '0.3152', '0.0000', '0.1313', '0.1939', '0.2945', '0.1281', '0.0000', '0.1348', '0.0000', '0.1521', '0.2944', '0.0000', '0.1988', '0.5401', '0.2464', '0.0000', '0.1376', '0.0201', '0.4651', '0.0651', '0.0587', '0.0000', '0.1002', '0.2052', '0.1705', '0.2143', '0.2442', '0.7530', '0.3695', '0.0623', '0.0000', '0.4199', '0.2091']

bm25_improvement = []
for bm25, ql in zip(bm25_ap, ql_ap):
    if(float(ql)!=0): 
        bm25_improvement.append((float(bm25) - float(ql)) / float(ql) * 100)
    else:
        bm25_improvement.append(0)

dpr_improvement = []
for dpr, ql in zip(dpr_ap, ql_ap):
    if(float(ql)!=0): 
        dpr_improvement.append((float(dpr) - float(ql)) / float(ql) * 100)
    else:
        dpr_improvement.append(0)


table = PrettyTable()
table.field_names = ["QueryNum", "QL (AP %6.ff)", "BM25 (AP %6.4f)", "Improvement BM25 (%)", "DPR (AP %6.4f)", "Improvement DPR (%)"]
for q, ql, bm25, bm25_imp, dpr, dpr_imp in zip(query_numbers, ql_ap, bm25_ap, bm25_improvement, dpr_ap, dpr_improvement):
    table.add_row([q, ql, bm25, bm25_imp, dpr, dpr_imp])

print(table)


            

        

def readQrelsFile(qrelsFile):
    qrelsData={}

    with open(qrelsFile, 'r') as file:
        for line in file:
            columns = line.strip().split()
            qName = columns[0]
            docId = columns[2]
            rel = float(columns[3])

            if qName not in qrelsData:
                qrelsData[qName] = {}

            qrelsData[qName][docId] = rel

    return qrelsData

def readTrecrunFile(trecrunFile):
    trecrunData = {}

    with open(trecrunFile, 'r') as file:
        for line in file:
            columns = line.strip().split()
            qName = columns[0]
            docId = columns[2]
            rank = float(columns[3])

            if qName not in trecrunData:
                trecrunData[qName] = {}

            trecrunData[qName][docId] = rank

    return trecrunData





if __name__ == '__main__':
    argv_len = len(sys.argv)
    runFile = sys.argv[1] if argv_len >= 2 else "msmarcosmall-bm25.trecrun"
    qrelsFile = sys.argv[2] if argv_len >= 3 else "msmarco.qrels"
    outputFile = sys.argv[3] if argv_len >= 4 else "my-msmarcosmall-bm25.eval"

    eval(runFile, qrelsFile, outputFile)
    # Feel free to change anything here ...

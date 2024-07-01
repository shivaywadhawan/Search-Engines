from numbers import Number
import sys
from collections import defaultdict
import gzip
import math



def read_links_file(file_name):
    inlinks = defaultdict(list)
    srcs=defaultdict(int)
    pages=[]
    # print("start")
    with gzip.open(file_name, 'rt') as file:
        for line in file:
            source, target = line.strip().split('\t')
            srcs[source]+=1
            inlinks[target].append(source)
            pages.append(source)
            pages.append(target)
        
        pages = list(set(pages))
        for i in pages:
            if i not in srcs:
                srcs[i]=0
            if i not in inlinks.keys():
                inlinks[i]=[]
    # print(outlinks)
    # print(inlinks)
            
    return srcs,inlinks,pages


def calculate_inlink_count(inlinks,pages):
    # print(links)
    temp = defaultdict(int)
    for src in inlinks.keys():
        # print(targets)
        temp[src] =len(inlinks[src])
    
    for i in pages:
        if i not in temp.keys():
            temp[i] =0
    
    return temp

def initialize_page_rank(lamb,pages):
    total_pages = len(pages)
    initial_score = 1 / total_pages
    page_rank = {}
    for i in pages:
        page_rank[i]=lamb*initial_score
    return page_rank


def page_rank_algorithmN(inlinks,outlinks_count,pages,lamb, max_iterations):
    iteration = 0
    page_rank = initialize_page_rank(1.00,pages)
    p=len(outlinks_count)
    # print(p)
    # print(inlinks)
    # print(outlinks)
    
    while iteration < max_iterations:
        new_page_rank = initialize_page_rank(lamb,pages)
        sum=0
        for src in outlinks_count:
            if outlinks_count[src] == 0:
                sum = sum + (1-lamb)*(page_rank[src]/p)
        for source, targets in inlinks.items():
            if len(targets)>0:
                for target in targets:
                    new_page_rank[source]=new_page_rank[source]+(1-lamb)*(page_rank[target]/outlinks_count[target])
            new_page_rank[source]=new_page_rank[source]+sum
            # else:
         
        page_rank = new_page_rank
        iteration+=1  
    return page_rank

def page_rank_algorithmConv(inlinks,outlinks_count,pages, lamb=0.20, tau=0.005):
    converged = False
    page_rank = initialize_page_rank(1.00,pages)
    p=len(outlinks_count)
   


    while not converged:
        new_page_rank = initialize_page_rank(lamb,pages)
        sum=0
        norm=0
        for src in outlinks_count:
            if outlinks_count[src] == 0:
                sum = sum + (1-lamb)*(page_rank[src]/p)
        for source, targets in inlinks.items():
            if len(targets)>0:
                for target in targets:
                    new_page_rank[source]=new_page_rank[source]+(1-lamb)*(page_rank[target]/outlinks_count[target])
            new_page_rank[source]=new_page_rank[source]+sum
            norm = norm + ((new_page_rank[source] - page_rank[source])*(new_page_rank[source] - page_rank[source]))
            # else:
        
        norm=math.sqrt(norm)
        if norm < tau:
            converged = True
        
        page_rank = new_page_rank
         

    return page_rank


def get_top_pages_by_inlink_count(outlinks,pages, k=100):
    # print(links)
    inlink_count = calculate_inlink_count(outlinks,pages)
    sorted_inlinks = sorted(inlink_count.items(), key=lambda x: (-x[1], x[0]))
    return [(page, idx + 1, count) for idx, (page, count) in enumerate(sorted_inlinks[:k])]


def get_top_pages_by_pagerank(links, page_rank, k=100):
    sorted_pagerank = sorted(page_rank.items(), key=lambda x: (-x[1], x[0]))
    return [(page, idx + 1, score) for idx, (page, score) in enumerate(sorted_pagerank[:k])]


def write_output_file(file_name, data):
    with open(file_name, 'w') as file:
        for item in data:
            file.write(f"{item[0]}\t{item[1]}\t{item[2]}\n")

def do_pagerank_to_convergence(input_file: str, lamb: float, tau: Number,
                               inlinks_file: str, pagerank_file: str, k: int):
    """Iterates the PageRank algorithm until convergence."""
    
    # Read links data
    srcs,inlinks,pages = read_links_file(input_file)
    outlinks_count=srcs
    
    # Run PageRank algorithm
    page_rank_scores = page_rank_algorithmConv(inlinks,outlinks_count,pages, lamb, tau)
    
    # Get top pages by inlink count
    top_pages_inlink = get_top_pages_by_inlink_count(inlinks,pages)
    
    # Get top pages by PageRank score
    top_pages_pagerank = get_top_pages_by_pagerank(inlinks, page_rank_scores)
    
    # Write output files
    write_output_file(inlinks_file, top_pages_inlink)
    write_output_file(pagerank_file, top_pages_pagerank)
    return


def do_pagerank_n_times(input_file: str,lamb:int, N: int, inlinks_file: str,
                        pagerank_file: str, k: int):
    """Iterates the PageRank algorithm N times."""
     # Read links data
    srcs,inlinks,pages = read_links_file(input_file) 
    outlinks_count=srcs
    
    # Run PageRank algorithm N times
    page_rank_scores = page_rank_algorithmN(inlinks,outlinks_count,pages,lamb,N)
    # links = page_rank_scores  # Update links with the latest PageRank scores
    
    # Get top pages by inlink count
    top_pages_inlink = get_top_pages_by_inlink_count(inlinks,pages)
    
    # Get top pages by PageRank score
    top_pages_pagerank = get_top_pages_by_pagerank(inlinks, page_rank_scores)
    
    # Write output files
    write_output_file(inlinks_file, top_pages_inlink)
    write_output_file(pagerank_file, top_pages_pagerank)


    return


def main():
    argc = len(sys.argv)
    input_file = sys.argv[1] if argc > 1 else 'links.srt.gz'
    lamb = float(sys.argv[2]) if argc > 2 else 0.2
    
    tau = 0.005
    N = -1  # signals to run until convergence
    if argc > 3:
        arg = sys.argv[3]
        if arg.lower().startswith('exactly'):
            N = int(arg.split(' ')[1])
        else:
            tau = float(arg)
    
    inlinks_file = sys.argv[4] if argc > 4 else 'inlinks.txt'
    pagerank_file = sys.argv[5] if argc > 5 else 'pagerank.txt'
    k = int(sys.argv[6]) if argc > 6 else 100
    
    if N == -1:
        do_pagerank_to_convergence(input_file, lamb, tau, inlinks_file, pagerank_file, k)
    else:
        do_pagerank_n_times(input_file,lamb, N, inlinks_file, pagerank_file, k)
    
    # ...


if __name__ == '__main__':
    main()

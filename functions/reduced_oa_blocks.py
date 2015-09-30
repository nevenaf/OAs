from itertools import combinations, permutations

def is_non_decreasing(seq):
    n = len(seq)
    for i in range(n):
        for j in range(i+1,n):
            if seq[i]>seq[j]:
                return False
    return True

def get_rows(k,n):
    order_of_row = {}
    row_of_order =[]
    
    idx = 0
    row = [0 for _ in range(k)]

    for comb in combinations(range(n), k-1): # no row of OA has any symbol twice
        for perm in permutations(range(k-1)): # order of symbols in a row
            for a in range(1,n): # first symbol in a row is not 0
                row[0] = a
                for i in range(k-1):
                    row[i+1] = comb[perm[i]]
                good = True
                
                # the first column of the first latin square is sorted
                if row[1]==0:
                    good = good and row[0]==row[2]
                if row[0]==row[2]:
                    good = good and row[1]==0
                
                # order the latin squares by the second values in the first column
                if good and (row[0]==1 and row[1]==0 and row[2]==1):
                    good = is_non_decreasing(row[3:k])
                
                if good:
                    rowt  = tuple(row)
                    order_of_row.update({rowt : idx})
                    row_of_order.append(rowt)
                    idx += 1
    return [order_of_row,row_of_order]

def get_pairs(k,n):
    ''' assumes t=2 '''
    
    order_of_pair = {}
    pair_of_order =[]
        
    idx = 0
    c1 = 0
    for a1 in range(1,n):
        for c2 in range(1,k):
            for a2 in range(n):
                pair = (c1,a1,c2,a2)
                order_of_pair.update({pair : idx})
                pair_of_order.append(pair)
                idx += 1  
    for c1 in range(1,k):
        for c2 in range(c1+1, k):
            for a1 in range(n):
                for a2 in range(a1+1,n):
                    pair = (c1,a1,c2,a2)    
                    order_of_pair.update({pair : idx})
                    pair_of_order.append(pair)
                    idx += 1 
                    
                    pair = (c1,a2,c2,a1)    
                    order_of_pair.update({pair : idx})
                    pair_of_order.append(pair)
                    idx += 1
    return [order_of_pair,pair_of_order]
    
   

def pair_covered(pair, row):
    ''' assumes t=2'''
    return row[pair[0]]==pair[1] and row[pair[2]]==pair[3]

def enter_chosen_row(k,chosen_row, row_of_order, pair_of_order):
    new_row_of_order = [row for row in row_of_order if not rows_intersect(k,row,chosen_row)]
    new_pair_of_order = [pair for pair in pair_of_order if not pair_covered(pair,chosen_row)]
    return [new_row_of_order,new_pair_of_order]


def rows_intersect(k,row1,row2):
    ''' t=2 assumed'''
    for i in range(k):
        for j in range(i+1,k):
            if row1[i]==row2[i] and row1[j]==row2[j]:
                return True
    return False


def enter_chosen_row(k,chosen_row, row_of_order, pair_of_order):
    new_row_of_order = [row for row in row_of_order if not rows_intersect(k,row,chosen_row)]
    new_pair_of_order = [pair for pair in pair_of_order if not pair_covered(pair,chosen_row)]
    return [new_row_of_order,new_pair_of_order]
              
              

def get_num_symb_per_col(k,n,subarray):
    # reduced form assumption
    mat = [[n for v in range(n)]] + [[n-1 for v in range(n)] for c in range(k-1)]
    mat[0][0]=0
    
    for row in subarray:
        for c in range(k):
            mat[c][row[c]] -= 1
    return mat

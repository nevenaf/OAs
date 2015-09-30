from gurobipy import * 
import multiprocessing as mp
from itertools import combinations

def get_coverage(t, row):
    k = len(row)
    tuples = []
    pair = [0 for _ in range(2*t)]

    for comb in combinations(range(k),t):
        for i in range(t):
            pair[2*i] = comb[i]
            pair[2*i+1] = row[comb[i]] 
        tuples.append(tuple(pair))      
    return tuples

def get_indices_of_covered_pairs(t,row,order_of_pair):
    indices = [order_of_pair[pair] for pair in get_coverage(t,row)]    
    return indices 


def get_incident_rows(t, k, n, order_of_row, order_of_pair):
    num_pairs = len(order_of_pair)
    incidence_mat = [[] for _ in range(num_pairs)]
    
    for row in order_of_row:
        pair_idx = get_indices_of_covered_pairs(t,row,order_of_pair)
        row_idx = order_of_row[row]
        for pair in pair_idx:
            incidence_mat[pair].append(row_idx)
    return incidence_mat 

def min_reduced_oa(k,n,order_of_row, row_of_order, order_of_pair, pair_of_order, len_subarray, sym_col_count, object_type, lin_relax = False, print_out=False,time_out=600):
    ''' object_type = packing, covering, oa '''
    
    if object_type not in [0,1,2]:
        print 'ERROR: object type is incorrect'
        exit()
    
    t = 2
    
    num_pairs = len(pair_of_order)
    num_rows = len(row_of_order)
    
    p = Model("min_reduced_ca")
    p.setParam("OutputFlag", 0)
    p.setParam("LogToConsole", 0)
    p.setParam("LogFile", "")
    p.setParam("Threads", mp.cpu_count())
    p.params.timelimit = time_out
    
    # add variables
    if lin_relax:
        y = [p.addVar(lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS) for _ in range(num_rows)]
    else:
        y = [p.addVar(vtype=GRB.BINARY) for _ in range(num_rows)]
    p.update()

    # add constraints
    incident_rows = get_incident_rows(t, k, n, order_of_row, order_of_pair) 
    
    # add constraint for count of vertices in columns
    total = [[0 for v in range(n)] for c in range(k)]
    for i in range(num_rows):
        row = row_of_order[i]
        for c in range(k):
            total[c][row[c]] += y[i]
    for c in range(k):
        for v in range(n):
            if sym_col_count[c][v]>0:
                if object_type==0:
                    p.addConstr(total[c][v] <= sym_col_count[c][v])
                elif object_type==1:
                    p.addConstr(total[c][v] >= sym_col_count[c][v])
                else:
                    p.addConstr(total[c][v] == sym_col_count[c][v])


    # add constraints for pair coverage
    for po in range(num_pairs):
        if len(incident_rows[po])==0:
            print 'error: pair ', pair_of_order[po], ' is not covered by any row'
            exit()
        total = 0    
        for i in incident_rows[po]:
            total += y[i]
        if object_type==0:
            p.addConstr(total <= 1)
        elif object_type==1:
            p.addConstr(total >= 1)
        else:
            p.addConstr(total == 1)    
    
    # add constraints for the bounds on the number of rows        
    if object_type==0:
        p.setObjective(sum(y), GRB.MAXIMIZE)
    elif object_type==1:
        p.setObjective(sum(y), GRB.MINIMIZE)
    else:
        p.addConstr(sum(y) == n*(n-1)-len_subarray) 

    p.update()
    print 'num of vars:', p.NumVars
    print 'num of constraints:', p.NumConstrs
    
    p.optimize()
    status = p.status
    
    if status == GRB.status.OPTIMAL:
        yx = p.getAttr('x', y)
        
        if lin_relax:
            return [1,yx]
        
        else:
            ca = [row_of_order[i] for i in range(num_rows) for _ in range(int(yx[i]))]
        
            if print_out == True:
                print ''        
                print 'optimal oa(',t,k,n,') with', len(ca),'rows:'
                for row in ca:
                    print row
                print ''

            return [1,ca]
        
    if status == GRB.status.INFEASIBLE:
        if print_out==True:
            print 'Infeasible! :)'
            print ''    
        return [0, []]
        
    if status == GRB.status.TIME_LIMIT:
        if print_out==True:
            print 'Time out'
            print ''    
        return [-1, []]
        
    return [-2,status] 

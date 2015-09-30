import time
from functions.reduced_oa_blocks import *
from functions.milp import *
from functions.subarray_functions import *
import cPickle as pickle

t = 2
print 'Integer program for finding an orthogona/packing/covering array in reduced form'
print ''
print '*** Note: efficient only for small values of parameters. ***'
print ''
k = int(raw_input("Enter number of columns: "))
n = int(raw_input("Enter number of symbols: "))

lin_relax = False
object_type = raw_input("Enter type [packing, covering, oa]: ")
ot = -1
if object_type=='packing':
    save_file = 'optimal_pa_k'+str(k)+'_n'+str(n)+'.p'
    ot = 0
elif object_type=='covering':
    save_file = 'optimal_ca_k'+str(k)+'_n'+str(n)+'.p'
    ot = 1
elif object_type=='oa':
    save_file = 'optimal_oa_k'+str(k)+'_n'+str(n)+'.p'
    ot = 2
else:
    print 'object type must be one of the following: packing, covering, oa'
    print ''
    exit()


lin_relax_str  = raw_input("Linear relaxation (L) or Integer program (I)? ").strip()
if lin_relax_str[0] in ['L', 'l']:
    lin_relax = True
elif lin_relax_str[0] in ['I', 'i']:
    lin_relax = False
else:
    print 'You must enter either L or I.'
    print ''
    exit()

time_out = 3600    
time_out_str = raw_input("Enter maximum execution time in seconds. Default is 3600s. ").strip()
if time_out_str != '':
    time_out = int(time_out_str)

directory = './'
file_name = ''
sub_array_str = raw_input('Do you wish to specify a subset of rows that must be contained in the array? [Y/N] ').strip()
if len(sub_array_str)>0 and sub_array_str[0] in ['Y', 'y']:
    directory = raw_input('Enter directory of the file which contains the subarray: ')
    file_name = raw_input('Enter the name of the file with the subarray (must be .p file): ')
   
print_out = False

print ''
print 'execution started on ', (time.strftime("%d/%m/%Y")),'at',(time.strftime("%H:%M:%S"))
print ''

order_of_row, row_of_order = get_rows(k,n)
order_of_pair, pair_of_order = get_pairs(k,n)
print 'oa(k=', k, 'n=', n, ')'
print '----------------------'

subarray = []
if file_name!='':
    subarray = pickle.load(open(directory+file_name ,'r'))
    
time_start = time.time()

len_subarray = len(subarray)    
sym_col_count = get_num_symb_per_col(k,n,subarray)

if len_subarray>0:
    print 'subarray:'
    for row in subarray:
        print row

# get the subset of rows and pairs which are still in the game
new_row_of_order = [row for row in row_of_order]
new_pair_of_order = [pair for pair in pair_of_order]
for row in subarray:
    new_row_of_order,new_pair_of_order = enter_chosen_row(k,row, new_row_of_order, new_pair_of_order)
    
new_order_of_row = { row:idx for idx,row in enumerate(new_row_of_order)}
new_order_of_pair = { pair:idx for idx,pair in enumerate(new_pair_of_order)}

ans = min_reduced_oa(k,n, new_order_of_row, new_row_of_order, new_order_of_pair, new_pair_of_order,  len_subarray, sym_col_count, ot, lin_relax, print_out,time_out)

if ans[0]==1:
    print ''
    print 'Optimal solution found.'
    ca = []
    if lin_relax:
        yx = ans[1]
        print 'linear relaxation returned objective value =', sum(yx)
        print 'result format: [array of [row, returned value of the variable correspondint to the row]]'
        ca = [[new_row_of_order[i], yx[i]] for i in range(len(new_row_of_order))]
    if len(ans[1])>0:
        ca = [tuple([0]+[v for _ in range(k-1)]) for v in range(n)]
        ca = ca + subarray
        ca = ca + ans[1]
        print 'size of the found array =', len(ca)
        
    print '******* saving result in the file '+ directory+ save_file+' *******'
    pickle.dump(ca, open(directory+save_file, 'w'))

elif ans[0]==0: 
    print 'No feasible solution.'   
elif ans[0]==-1:
    print 'Time elapsed...'
    print ''
else: 
    print 'Gurobi optimizer returned status: ', ans[1]

print ''          


print ''
print 'execution ended on ', (time.strftime("%d/%m/%Y")),'at',(time.strftime("%H:%M:%S")) , '(running time: ', time.time()-time_start, 's)'


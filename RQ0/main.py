import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from tools.ezr import *
from tools.stats import *

file_directory = sys.argv[1] if len(sys.argv) > 1 else "data/optimize/misc/auto93.csv"
repeats = 20

all_data = Data(csv(file_directory))
ys      = [disty(all_data,row) for row in all_data.rows]
b4      = adds(ys)
win     = lambda v: int(100*(1 - (v - b4.lo)/(b4.mu - b4.lo)))
b4_wins = adds([win(k) for k in ys])

half = int(0.5 * len(all_data.rows))
suggested_optima, suggestion_error = [], []
for rand_seed in range(repeats):
    ## New draw from data
    the.seed    = rand_seed
    random.seed(the.seed)
    shuffled_rows = random.sample(all_data.rows, len(all_data.rows)) 
    train, holdout = clone(all_data, shuffled_rows[:half]), clone(all_data, shuffled_rows[half:])
    referenced_optima = win(min(disty(all_data, row) for row in holdout.rows))

    ## Initial Setting
    the.Budget  = 20
    the.acq     = "xploit"
    the.leaf    = 2
    the.Impurity= "entropy"
    the.Check   = 10    
    
    labels = likely(train)
    tree   = Tree(clone(train, labels))
    top_rows = sorted( [(treeLeaf(tree, row).mu, row) for row in holdout.rows], key=lambda x: x[0])[:the.Check]
    suggested_optima.append( win( sorted([disty(all_data, row) for _, row in top_rows])[0] ) )
    suggestion_error.append(referenced_optima - suggested_optima[-1])

print(f"Dataset, {file_directory.split("/")[-1][:-4]}")
print(f"All Sugg., {[round(s,2) for s in sorted(suggested_optima)]}")

## For Evaluating Quality:
print(f"Sugg. Med, {sorted(suggested_optima)[repeats//2]:.2f}")
## For Evaluating Instability:
print(f"Sugg. Std, {adds(suggested_optima).sd:.2f}")

## Dataset's own std
print(f"dataset Std, {b4_wins.sd:.2f}")

## For Evaluating Quality:
print(f"Error, {sum([s**2 for s in sorted(suggestion_error)]) ** 0.5:.2f}")
# ## For Evaluating Instability:
# print(f"Error. Std, {adds(suggestion_error).sd:.2f}")
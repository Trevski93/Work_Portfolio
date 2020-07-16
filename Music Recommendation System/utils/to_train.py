import itertools

alphas = ('0.5', '1.0', '1.5')
ranks = ('8', '10', '12', '20')
regs = ('0.001', '0.01', '0.1', '1.0')
params_list = set(itertools.product(alphas, ranks, regs))
 
filepath = 'already_trained.txt'  
with open(filepath) as fp:  
	line = fp.readline()
	while line:
		splits = line.strip().split('_')
		params_list.discard(tuple([splits[i] for i in (7,3,5)]))

		line = fp.readline()

print(('; ').join(['spark-submit --driver-memory 10g --executor-memory 10g --num-executors 10 train.py --user tim225 --train_file train_full_indexed --alpha %s --rank %s --reg %s --all_or_one one >> logs.txt' % params \
	for params in params_list]))
import pandas as pd
columns = ['rank', 'reg', 'alpha', 'MAP']
df = pd.DataFrame(columns=columns)

with open('./results.txt') as f:  
   line = f.readline()
   i = 0
   while line:
	   params = line.strip().split('_')[3:]
	   MAP = float(f.readline())
	   
	   line = f.readline()
	   df.loc[i] = [*params, MAP]

	   i += 1

df.sort_values(by='MAP', ascending=False).to_csv('results.csv')
for col in columns[:-1]:
	df.groupby(col).max()[['MAP']].sort_values(
		by='MAP', ascending=False).to_csv('top_%s.csv' % col)
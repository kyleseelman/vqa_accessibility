samples = {'LQI':[], 'IVE':[], 'INV':[], 
		'DFF':[], 'AMB':[], 'SBJ':[], 'SYN':[], 'GRN':[], 'SPM':[], 'diff_OTH':[], 
		'TXT':[], 'OBJ':[], 'COL':[], 'CNT':[], 'skill_OTH':[]}
for data in datas:
	if float(data['ALBEF score']) > 0.35: continue
	for cate in samples:
		if len(samples[cate]) >10: continue
		if data[cate] != 1: continue
		samples[cate].append(data)
		break
for key in samples:
	ss = samples[key]
	for s in ss:
		sample = [s['qid'],s['imageid'],s['question'],s['src_dataset'],s['answer_type'],s['ALBEF answer'],s['ALBEF score']]
		print(key, '\t','\t'.join(sample))

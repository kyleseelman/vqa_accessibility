import sys
import re
import csv
import json


fp = open("./output/vizwiz/result/vqa_result_epoch7_a4000.json", "r") 
answer_dict = json.load(fp)
fp.close()

fp = open("../openvqa/data/vizwiz/raw/val.json")
ground_truth = json.load(fp)
fp.close()

#print(answer_dict[0])
#print(ground_truth)

ques_id = []
res_ans = {}
for ques in answer_dict:
    res_ans[ques['question_id']] = ques['answer']
    ques_id.append(ques['question_id'])
#print(ques_id)
#print(res_ans)

answer_set = {}
for ques in ground_truth:
    #print(ques)
    answer_set[ques['image']] = {'answers' : ques['answers'], 'question': ques['question'], 'id': ques['image']}
#print(answer_set)

#for ques in answer_set:
#    answers = answer_set[ques]['answers']
    #print(answer_set[ques]['answers'])
accQA       = []
with open('vizwiz_answers_not_ft.csv', 'w', newline='') as csvfile:
    for ques in ques_id:

        res = res_ans[ques]
        #print(res)
        gtAcc  = []
        gtAnswers = [ans['answer'] for ans in answer_set[ques]['answers']]
        #print(gtAnswers)
        #print("break")
        #print(answer_set[ques]['answers'])
        for gtAnsDatum in answer_set[ques]['answers']:
            #print("Ans DATUM: ", gtAnsDatum)
            # the dict of answer/answer_confidence that are differnet than gtAnsDatum
            otherGTAns = [item for item in answer_set[ques]['answers'] if item is not gtAnsDatum]
            #print("otherGTAns: ", otherGTAns)
            # gives the set (10) of all answers for question
            # list for whole set of true/false
            matchingAns = [item for item in otherGTAns if item['answer']==res]
            #print(matchingAns)
            acc = min(1, float(len(matchingAns))/3)
            #print(acc)
            gtAcc.append(acc)
        #break
        #ansType = ground_truth[quesId]['answer_type']
        avgGTAcc = float(sum(gtAcc))/len(gtAcc)
        accQA.append(avgGTAcc)
    #print(accQA)
        writer = csv.writer(csvfile)
        writer.writerow([answer_set[ques]['question'], res, avgGTAcc, answer_set[ques]['id']])

print(round(100*float(sum(accQA))/len(accQA), 2))

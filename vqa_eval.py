import sys
import re
import csv
import json


fp = open("./vqa_small_result_epoch7.json", "r") 
answer_dict = json.load(fp)
fp.close()

fp = open("../openvqa/data/vqa/raw/v2_OpenEnded_mscoco_val2014_questions.json")
questions = json.load(fp)
fp.close()

fp = open("../openvqa/data/vqa/raw/v2_mscoco_val2014_annotations.json")
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
ground_truth = ground_truth['annotations']
questions = questions['questions']
for temp, temp2 in zip(ground_truth, questions):
    #print(temp)
    answer_set[temp['question_id']] = {'answers' : temp['answers'], 'question': temp2['question'], 'id':temp2['question_id']}
#print(answer_set)

#for ques in answer_set:
#    answers = answer_set[ques]['answers']
    #print(answer_set[ques]['answers'])
accQA = []
with open('answers.csv', 'w', newline='') as csvfile:
    for ques in ques_id:

        res = res_ans[ques]
        print(res)
        gtAcc = []
        gtAcc  = []
        gtAnswers = [ans['answer'] for ans in answer_set[ques]['answers']]
        print(gtAnswers)
        print("break")
        print(answer_set[ques]['answers'])
        for gtAnsDatum in answer_set[ques]['answers']:
            print("Ans DATUM: ", gtAnsDatum)
            # the dict of answer/answer_confidence that are differnet than gtAnsDatum
            otherGTAns = [item for item in answer_set[ques]['answers'] if item != gtAnsDatum]
            print("otherGTAns: ", otherGTAns)
            # gives the set (10) of all answers for question
            # list for whole set of true/false
            matchingAns = [item for item in otherGTAns if item['answer']==res]

            acc = min(1, float(len(matchingAns))/3)
            gtAcc.append(acc)
        break
        #ansType = ground_truth[quesId]['answer_type']
        avgGTAcc = float(sum(gtAcc))/len(gtAcc)
        accQA.append(avgGTAcc)
    #print(accQA)
        writer = csv.writer(csvfile)
        writer.writerow([answer_set[ques]['question'], res, avgGTAcc, answer_set[ques]['id']])

print(round(100*float(sum(accQA))/len(accQA), 2))
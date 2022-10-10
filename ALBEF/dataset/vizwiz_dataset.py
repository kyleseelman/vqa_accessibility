import os
import json
import random
from PIL import Image
from torch.utils.data import Dataset
from dataset.utils import pre_question


class vizwiz_dataset(Dataset):
    def __init__(self, ann_file, transform, vqa_root, eos='[SEP]', split="train", max_ques_words=15, answer_list=''):
        self.split = split        
        self.ann = []
        for f in ann_file:
            self.ann += json.load(open(f,'r'))

        self.transform = transform
        self.vqa_root = vqa_root
        #self.vg_root = vg_root
        self.max_ques_words = max_ques_words
        self.eos = eos
        
        if split=='test':
            self.max_ques_words = 50 # do not limit question length during test
            self.answer_list = json.load(open(answer_list,'r'))    
                
        
    def __len__(self):
        return len(self.ann)
    
    def __getitem__(self, index):    
        
        ann = self.ann[index]
        #print(ann)
        
        #taset']=='vqa':
        image_path = os.path.join(self.vqa_root,ann['image'])   
        #print(image_path)   
        
        if self.split == 'test':
            image_path = os.path.join("../openvqa/vqa_val/val_vizwiz/", ann['image'])

        image = Image.open(image_path).convert('RGB')   
        image = self.transform(image)          
        
        if self.split == 'test':
            question = pre_question(ann['question'],self.max_ques_words)  
            #print(question) 
            question_id = ann['image']            
            return image, question, question_id


        elif self.split=='train':                       
            
            question = pre_question(ann['question'],self.max_ques_words)        
            #print(question)
            
            answer_weight = {}
            for answer in ann['answers']:
                if answer['answer'] in answer_weight.keys():
                    answer_weight[answer['answer']] += 1/10
                else:
                    answer_weight[answer['answer']] = 1/10

            answers = list(answer_weight.keys())
            weights = list(answer_weight.values())
 

            answers = [answer+self.eos for answer in answers]
            #print(answers)
            #print("Made it to ends")
            return image, question, answers, weights
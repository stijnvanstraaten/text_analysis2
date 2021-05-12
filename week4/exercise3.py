from collections import Counter
from nltk.metrics import ConfusionMatrix
import os
import sys


directories_p49 = os.listdir("p49")
directories_p50 = os.listdir("p50")


_, annotation_setting, annotated_file_1, annotated_file_2 = sys.argv
tag_list_1, tag_list_2, annotated_text_1, annotated_text_2 = [], [], [], []
tag_set = set({})


for dir in directories_p49:
    path = "p49/" + dir + "/"
    with open(path + annotated_file_1, "r") as text:
        text = text.read()
    annotated_text_1 += text.split("\n")

    with open(path + annotated_file_2, "r") as text:
        text = text.read()
    annotated_text_2 += text.split("\n")

for dir in directories_p50:
    path = "p50/" + dir + "/"
    with open(path + annotated_file_1, "r") as text:
        text = text.read()
    annotated_text_1 += text.split("\n")

    with open(path + annotated_file_2, "r") as text:
        text = text.read()
    annotated_text_2 += text.split("\n")
    
for i in range(len(annotated_text_1)):
    annotated_text_1[i] = annotated_text_1[i].split(" ")
    if annotated_text_1[i][0] != "":
        try:
            annotation_tag = annotated_text_1[i][5]
            if annotation_setting == "1":
                tag_list_1.append(annotation_tag)
                tag_set.add(annotation_tag)
            else:
                tag_list_1.append("Tagged")
                tag_set.add("Tagged")
        except:
            tag_list_1.append("None")
            tag_set.add("None")

for i in range(len(annotated_text_2)):
    annotated_text_2[i] = annotated_text_2[i].split(" ")
    if annotated_text_2[i][0] != "":
        try:
            annotation_tag = annotated_text_2[i][5]
            if annotation_setting == "1":
                tag_list_2.append(annotation_tag)
                tag_set.add(annotation_tag)
            else:
                tag_list_2.append("Tagged")
                tag_set.add("Tagged")
        except:
            tag_list_2.append("None")
            tag_set.add("None")


cm = ConfusionMatrix(tag_list_1, tag_list_2)

print(cm)


true_positives = Counter()
false_negatives = Counter()
false_positives = Counter()

print(tag_set)
for i in tag_set:
    for j in tag_set:
        if i == j:
            true_positives[i] += cm[i,j]
        else:
            false_negatives[i] += cm[i,j]
            false_positives[j] += cm[i,j]

print("TP:", sum(true_positives.values()), true_positives)
print("FN:", sum(false_negatives.values()), false_negatives)
print("FP:", sum(false_positives.values()), false_positives)
print("")

print(tag_set)
for i in sorted(tag_set):
    if true_positives[i] == 0:
        precision = "error - devision by zero"
        recall = "error - devision by zero"
        fscore = 0
    else:
        precision = true_positives[i] / float(true_positives[i]+false_positives[i])
        recall = true_positives[i] / float(true_positives[i]+false_negatives[i])
        fscore = 2 * (precision * recall) / float(precision + recall)
    print(i)
    print("precision: " + str(precision))
          
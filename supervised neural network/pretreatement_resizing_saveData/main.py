__author__ = 'yxu01'
from dataset_GENER_copy import saveData

imageAdd = [];
imageAdd.append(raw_input("plese enter TranningSet address :"))
imageAdd.append(raw_input("plese enter TestSet address:"))
imageAdd.append(raw_input("plese enter ValidationSet address:"))
saveData(imageAdd)






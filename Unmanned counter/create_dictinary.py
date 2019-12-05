user_dic = {"id": [], "pw":[]}
class_name_dic = []
label_dic = []

import numpy as np

np.save("./labels", user_dic)
np.save("./class_names", class_name_dic)
np.save("./embeddings", class_name_dic)

test_dic = np.load("./user_dic.npy")
# ******************************************************************************
# dataset.py
#
# Date      Name       Description
# ========  =========  ========================================================
# 2/25/19   Paudel     Initial version,
# ******************************************************************************

class Dataset():
    dataset_name = None
    file_name = None
    spam_id = []
    feature_file = None
    available_dataset = []
    subgraph_list = {}

    def __init__(self):
        print("\n\n----- Preparing Dataset ----")
        pass

    def initialize_dataset(self, d):
        try:
            ds = Dataset()
            ds.dataset_name = d[0]
            ds.file_name = d[1]
            ds.spam_id = d[2]
            ds.feature_file = d[3]
            print('----- Dataset [ %s ] Created Successfully----' % (ds.dataset_name))
            return ds
        except Exception as e:
            print('----- Couldnot Create Dataset [ %s ] ----' % (d[0]))
            return None

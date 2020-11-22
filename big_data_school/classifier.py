import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_roc_curve, log_loss, plot_precision_recall_curve
import matplotlib.pyplot as plt


tabular_data = pd.read_csv("./tabular_data.csv")
hashed_feature = pd.read_csv("./hashed_feature.csv")
train_data = pd.read_csv("./train.csv")
test_data = pd.read_csv("./test.csv")

train_size = 4084
periods_num = 12
total_size = max(tabular_data['id']) + 1

processed_tabular = tabular_data.drop(columns=['feature_41', 'feature_25', 'feature_31', 'feature_34'])
# processed_tabular = processed_tabular.drop(columns=['feature_1', 'feature_6'])
deriv_array = [len(hashed_feature['feature_50'][hashed_feature['id'] == id]) for id in range(total_size)]
hashed_deriv = pd.DataFrame({'id': list(range(total_size)), 'hashed_deriv': deriv_array})
processed_tabular = processed_tabular.merge(how='left', right=hashed_deriv)
# processed_tabular = processed_tabular.merge(how='left', right=train_data)
# nanfree_tabular = processed_tabular.dropna(axis='columns')

cols = processed_tabular.columns
feature_abundance = {}
for col in cols:
    if 'feature' in col:
        feature_abundance[col] = len(pd.unique(processed_tabular[col]))

categorical_limit = 10
abundance_limit = train_size
categorical_features = [col for col in feature_abundance.keys() \
                        if feature_abundance[col] < categorical_limit]
numerical_features = [col for col in feature_abundance.keys() \
                      if feature_abundance[col] >= categorical_limit]
# numerical_features += ['period', 'hashed_deriv']
numerical_features += ['hashed_deriv']

processed_tabular = processed_tabular.fillna({col: processed_tabular[col].median() \
                   for col in numerical_features})
processed_tabular = processed_tabular.fillna({col: processed_tabular[col].value_counts().index[0] \
                  for col in categorical_features})

aggr_features = pd.DataFrame({'id': list(range(total_size)), 'hashed_deriv': deriv_array})
for col in numerical_features:
    aggr_features.insert(loc=2, column=col + 'Avg', \
                         value=[np.mean(processed_tabular[col][processed_tabular['id'] == id]) \
                                for id in range(total_size)])
    aggr_features.insert(loc=2, column=col + 'Std', \
                         value=[np.std(processed_tabular[col][processed_tabular['id'] == id]) \
                                for id in range(total_size)])

gathered_data = processed_tabular.merge(how='left', right=aggr_features)
input_data = gathered_data[gathered_data.id < train_size]
# input_data = aggr_features[aggr_features.id < train_size]
bare_num = np.array(input_data)
# bare_num = np.array(input_data[[col + 'Avg' for col in numerical_features] \
#                                + [col + 'Std' for col in numerical_features]])
input_data = input_data.merge(how='left', right=train_data)

train_num_X, valid_num_X, train_y, valid_y \
= train_test_split(bare_num, input_data['target'], test_size=0.33, random_state=42)

cross_valid_X, test_valid_X, cross_valid_y, test_valid_y \
= train_test_split(valid_num_X, valid_y, test_size=0.5)#, random_state=42)

# classifier2 = RandomForestClassifier(n_estimators=300, max_depth=4, random_state=0)
classifier2 = RandomForestClassifier(n_estimators=800, max_depth=10, random_state=0)
classifier2.fit(train_num_X, train_y)
forest_disp2 = plot_roc_curve(classifier2, valid_num_X, valid_y)
forest_disp_train = plot_roc_curve(classifier2, train_num_X, train_y)
# forest_disp_valid = plot_roc_curve(classifier2, cross_valid_X, cross_valid_y)
# forest_disp2 = plot_roc_curve(classifier2, test_valid_X, test_valid_y)

test_X = gathered_data[gathered_data.id >= train_size]
test_y = classifier2.predict(test_X)
test_data['score'] = test_y[::12]
test_data.to_csv('./classified.csv', index=False)

from training.utils import utils
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer


def process_data(dataset_filepath, x, y):
  #validate input
  input_list = [
    ('x', x, str),
    ('y', y, str)
  ]
  utils.validate_inputs(input_list)

  # 1. Load the dataset
  df = utils.read_dataset(dataset_filepath)

  # 2. Preprocess: split data
  df_attribute = df[[x]]
  df_label = df[y]

  # 3. Split into train and test sets
  X_train, X_test, y_train, y_test = train_test_split(df_attribute, df_label, test_size=0.2, random_state=42)
  
  # 4. Convert text to TF-IDF vectors
  vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2))
  X_train_vec = vectorizer.fit_transform(X_train[x])
  X_test_vec = vectorizer.transform(X_test[x])

  return X_train_vec, y_train, X_test_vec, y_test, vectorizer



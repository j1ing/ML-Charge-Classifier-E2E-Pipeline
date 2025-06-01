from sklearn.linear_model import LogisticRegression

def train(X_train_vec, y_train, iter_count):
  #Train classifier
  model = LogisticRegression(max_iter=iter_count)
  model.fit(X_train_vec, y_train)

  return model
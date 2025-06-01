from sklearn.metrics import classification_report

def report(y_test, y_pred):
  return classification_report(y_test, y_pred, output_dict=True)
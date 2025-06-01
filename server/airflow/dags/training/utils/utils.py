import pandas as pd
import openpyxl as xl

def read_dataset(filepath, sheetname = None):
  ext = filepath.split('.')[-1].lower()

  if ext == 'csv':
    df = pd.read_csv(filepath)

  elif ext == 'xlsx':
    if sheetname == None:
      raise ValueError("sheetname cannot be None type if reading an excel file.")
    
    # Load the Excel workbook and verify sheet name
    wb = xl.load_workbook(filepath, read_only=True)
    if sheetname not in wb.sheetnames:
      raise ValueError("sheetname not found in excel file.")
    
    df = pd.read_excel(filepath,sheet_name=sheetname)

  else:
    raise Exception(f"Unsupported file type '{ext}'. Only supporting csv or xlsx")
  
  return df


def validate_inputs(input_list):
  error_list = []
  for input_name, input_value, expected_type in input_list:
    if not isinstance(input_value, expected_type):
      error_list.append((input_name, expected_type.__name__, type(input_value).__name__))

  if len(error_list) != 0:
    formatted = ', '.join([f"{name} (expected {exp}, got {got})" for name, exp, got in error_list])
    raise Exception(f"Invalid input types: {formatted}")

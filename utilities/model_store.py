import pickle

def dump(Q, file_path):
  with open(file_path, 'wb') as file:
    pickle.dump(Q, file)

def load(file_path):
  with open(file_path, 'rb') as file:
    return pickle.load(file)
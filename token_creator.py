import pickle

def create_new_file(file, token):

    with open(file, 'wb') as f:

        pickle.dump(
            {
                'token':str(token)
            }, f
        )
def create_new_file_from_dict(file, dict):

    with open(file, 'wb') as f:

        pickle.dump(
            dict, f
        )

import pickle

def create_new_file(file, token):

    with open(file, 'wb') as f:

        pickle.dump(
            {
                'token':str(token)
            }, f
        )

if __name__ == '__main__':

    create_new_file('.beta','token')

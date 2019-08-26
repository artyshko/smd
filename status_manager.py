import pickle

class Manager():

    @staticmethod
    def setStatus(status=True):

        with open('.status', 'wb') as f:

            pickle.dump(
                {
                    'status':status
                }, f
            )
    @staticmethod
    def getStatus():

        with open('.status', 'rb') as f:
                data = pickle.load(f)

        return data['status']

if __name__ == '__main__':

    Manager.setStatus(True)

    print(Manager.getStatus())
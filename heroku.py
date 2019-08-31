import heroku3
import pickle


def restart():

    def getData():

        try:

            with open('.heroku_data', 'rb') as f:
                data = pickle.load(f)

            return data['token']

        except:

            sys.exit()
    
    try:

        heroku_conn = heroku3.from_key(getData())
        app = heroku_conn.apps()['smd-bot']
        dyno = app.dynos()[0]

        print('RESTARTING_DYNO:DONE')

        dyno.restart()

    except:

        print('RESTARTING_DYNO:ERROR')


if __name__ == '__main__':

    restart()

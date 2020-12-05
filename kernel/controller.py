__version__ = '1.7.2-st'

import os
import sys
import imp
import math
import types
import string
import shutil
import inspect
import logging
import argparse
import collections
from six import exec_
from pathlib import Path
from kernel.smdc.core import CORE
from abc import ABC, abstractmethod

sys.path.append('modules/addons')
#from genius.main import Genius
from tagc.main import TagEditor


logging.basicConfig(
    level=logging.INFO,
    format=f'SMD %(asctime)s [ %(levelname)-2s ] (%(name)s) [%(funcName)s] %(message)s'
)
_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(logging.INFO)

class ConfigHandler():

    _logger_cf = logging.getLogger("CF")

    __config_path__ = f"{os.path.abspath(os.getcwd())}/kernel/config/config"
    __config_data__ = f"{os.path.abspath(os.getcwd())}/kernel/config/data/"
    __config__ = None

    class init(object):

        @staticmethod
        def watch(_function_):
            def wrapper(*args):
                __result__ = _function_(*args)
                ConfigHandler._logger_cf.info(f'INIT [{__result__._cf_}]')
                _cf_, __module__ = ConfigHandler.get_config(__result__._cf_), imp.new_module('NDI=')
                exec_(CORE.core_filesystem_manager.init(f"{ConfigHandler.__config_data__}{_cf_}"), __module__.__dict__)
                __result__.__dict__['client'] = __result__.__dict__['client'](__module__.__dict__['_cf_'])
                del __module__
            return wrapper

        @staticmethod
        def raw(_function_):
            def wrapper(*args):
                __result__ = _function_(*args)
                ConfigHandler._logger_cf.info(f'INIT [{__result__._cf_}]')
                _cf_ = ConfigHandler.get_config(__result__._cf_)
                __result__.__dict__['client'] = __result__.__dict__['client'](_cf_)
                del _cf_
            return wrapper


    @staticmethod
    def __read_config__():
        with open(ConfigHandler.__config_path__, 'r') as config:
            __module__ = imp.new_module('config')
            exec_(config.read(), __module__.__dict__)
            ConfigHandler.__config__ = __module__


    @staticmethod
    def include_cf(__cf__):

        return CORE.core_filesystem_manager.include_cf(f"{ConfigHandler.__config_data__}{__cf__}")


    @staticmethod
    def get_config(conf):

        False if ConfigHandler.__config__ else ConfigHandler.__read_config__()
        return None if conf not in (ConfigHandler.__config__.__dict__) else ConfigHandler.__config__.__dict__[conf]


class DriverManager():

    _logger_drv = logging.getLogger("DRV")

    class AbstractClassAPI(ABC):

        __slots__ = [
            'domains',
            'routes',
            'callback'
            'link'
        ]

        @abstractmethod
        def preprocessor(_function_):
            pass

        @abstractmethod
        def confirm_link(self, link):
            pass

        @abstractmethod
        def get_track_info(self, link):
            pass

        @abstractmethod
        def get_album_info(self, link):
            pass

        @abstractmethod
        def get_playlist_info(self, link):
            pass


    @staticmethod
    def init():

        DriverManager._logger_drv.info('INIT Driver Manager')

        from modules.drivers import __init__ as modules
        __drivers__ = { key:val for (key,val) in modules.__self__.__dict__.items() if type(val) is types.ModuleType}

        for driver in __drivers__:

            __module__ = imp.load_source(driver,__drivers__[driver].__file__)

            DriverManager._logger_drv.info(f'INIT [{__module__.__module_name__}] v.{__module__.__version__}')
            setattr(DriverManager, __module__.__name__, __module__)

        DriverManager.__get_all_apis__()


    @staticmethod
    def __get_all_apis__():

        __drivers__ = { key:val for (key,val) in DriverManager.__dict__.items() if type(val) is types.ModuleType}

        setattr(DriverManager, 'api', [])

        for _ in __drivers__:

            all_classes_from_obj = { key:val for (key,val) in __drivers__[_].__dict__.items() if inspect.isclass(val)}
            has_api = [True if issubclass(all_classes_from_obj[_class_],DriverManager.AbstractClassAPI) else False for _class_ in all_classes_from_obj.keys()]

            DriverManager.api.append(_) if True in has_api else None


    @staticmethod
    def __enter__():
        DriverManager.init()

        return DriverManager


    @staticmethod
    def __exit__(exc_type, exc_val, exc_tb):

        pass


    @staticmethod
    def create_api_context(link=None):

        DriverManager.__exit__(None,None,None)

        for _api_ in DriverManager.api:
            _module_ = DriverManager.__dict__[_api_].API()
            if _module_.confirm_link(link=link):
                setattr(DriverManager, 'context', _module_)
                break


class DownloadManager():

    _cf_ = 'DEFAULT_DOWNLOADING_PATH'

    class Clasificator():

        def __init__(self, original, data):

            self.original_data = original
            self.original = f"{self.original_data['artist'][0]} {self.original_data['name']}"
            self.data = data

        def __enter__(self):

            return self

        def __exit__(self, exc_type, exc_val, exc_tb):

            pass

        def __tf__(self, _raw_text_):
            
            _splited_text_ = _raw_text_.split(' ')
            _tf_text_ = collections.Counter(_splited_text_)

            for i in _tf_text_:
                
                _tf_text_[i] = _tf_text_[i]/float(len(_splited_text_))
            
            return _tf_text_


        def __idf__(self, _word_, _corpus_):

            _sum_ = sum([1.0 for i in _corpus_ if _word_ in i])

            return math.log10(len(_corpus_)/_sum_) if _sum_ else .0
        
        def __calculate_tf_idf__(self):

            _o_tf_res_ = self.__tf__(self.original)
            _corpus_ = [i for i in self.data]

            final = 0
            calculated = {}

            for _c_item_ in self.data:

                calculated[_c_item_['name']] = 0
                _corpus_ = str(_c_item_['name']).split(' ')

                for _o_item_ in _o_tf_res_:

                    res = self.__idf__(_o_item_, _corpus_)
                    final += _o_tf_res_[_o_item_] * res

                diff = len(_corpus_) - len(_o_tf_res_)
                
                new = final - (math.log10(abs(diff)) if abs(diff) else 0)
                calculated[_c_item_['name']], final = new, 0
                _c_item_['_tf_idf_'] = new

        def normalize(self):

            self.__calculate_tf_idf__()

            item_d = self.original_data['duration_ms']

            for item in self.data:

                item_t = item['time'] if item['time'] else 0
                item_w = item['_tf_idf_']
                result = math.sqrt((item_d - item_t)**2 + (1 - item_w)**2)
                item['predict'] = result

            result = sorted(self.data, key = lambda i: i['predict'],reverse=False)
            '''for i in result:
                print(i['name'],i['_tf_idf_'],i['predict'],'\n')'''
            print('CLF:O[',self.original,'(',item_d,')]:P[',result[0]['name'],'(',result[0]['time'],')]')
            return result

    class ResultsHandler():

        def __init__(self, data):

            self.data = data
            self.keys = [key['name'] for key in self.data]


        def __enter__(self):

            return self


        def __exit__(self, exc_type, exc_val, exc_tb):

            pass


        def get_choice(self,original=None):

            print(f'\n\nOiginal: {original}\nTake your chioce:\n')

            print('0\t Cancel\n')

            _choice_ = None
            _it_ = 1

            for key in self.keys:
                print(_it_,'\t',key)
                _it_ += 1

            while not _choice_:

                _num_ = input('\nNumber> ')

                if str(_num_).isnumeric():

                    if 0 < int(_num_) < len(self.keys)+1:

                        _choice_ = self.keys[int(_num_)-1]
                        for key in self.data:
                            _choice_ = key if key['name'] == _choice_ else _choice_

                    elif int(_num_) == 0:
                        return False

            return _choice_


    @ConfigHandler.init.raw
    def init(self):

        self.client = self.config
        self.data = None
        self.lyrics_manager = None
        self.__ch__ = True

        return self


    def set_lyrics_manager(self, lyrics_manager):

        self.lyrics_manager = lyrics_manager


    def config(self, path):
        self.path = path


    def __enter__(self):

        self.init()
        CORE.init()

        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


    def get_api_callback(self, callback):

        self.data = callback
    

    def name_preprocessor(self, name):

        to_remove = dict((ord(char), None) for char in '\/*:<>|')
        str(name).translate(to_remove)

        return name


    def download(self):

        if not self.data:
            return False

        __tracks__ = []
        __results__ = []
        __final__ = []

        if 'tracks' in self.data.keys():
            while self.data['tracks']:
                __tracks__.append(self.data['tracks'].pop())
        else:
            __tracks__ = [self.data]

        for _track_ in __tracks__:

            _query_ = f'{_track_["artist"][0]} {_track_["name"]}'
            print('QUERY', _query_)
            _duration_ = _track_['duration_ms']
            _results_ = CORE.execute(
                'Client',
                'searchAll',
                (_query_,_duration_,)
            )

            for _result_ in _results_:
                if _result_:
                    __results__ += _result_

            with self.Clasificator(_track_,__results__) as clf:
                __final__ = clf.normalize()

            __l2d__ = __final__[-1]
            if self.__ch__:

                with self.ResultsHandler(__final__) as res:
                    __l2d__ = res.get_choice(original=f'{_track_["artist"][0]} {_track_["name"]}')

                    if not __l2d__:
                        continue

            _s_numb_ = __l2d__['s']
            _module_ = None

            for __module__ in CORE.get_all_included_modules():

                _module_ = __module__ if CORE.__dict__[__module__].Client().server_number == _s_numb_ else _module_

            CORE.__dict__[_module_].Client().download(__l2d__,_track_['uri'])

            print(_track_)

            _lyrics_ = self.lyrics_manager.get_lyrics(self.lyrics_manager,_track_['artist'][0], _track_['name']) if self.lyrics_manager else ''
            TagEditor.set_tags(_track_,_lyrics_)

            if ConfigHandler.get_config('MOVE'):

                name = f"{_track_['uri']}.mp3"
                path = ConfigHandler.get_config('DEFAULT_DOWNLOADING_PATH')
                move_to = f'{str(Path.home())}/Music' if not path else path
                fixed_name = self.name_preprocessor(f"{_track_['artist'][0]} - {_track_['name']}.mp3")

                print('FIXED NAME', fixed_name)

                if not Path(f"{move_to}/{fixed_name}").exists():
                    shutil.move(
                        f"cache/{_track_['uri']}/{_track_['uri']}.mp3",
                        f"{move_to}/{fixed_name}"
                    )
                try:
                    shutil.rmtree(f"cache/{_track_['uri']}")
                except:pass


class CommandLineInterfaceManager():

    _cf_ = 'CLI'

    @ConfigHandler.init.watch
    def init(self):

        self.client = self.__cl
        return self

    def __cl(self, val):

        self.header = val

    def info(self):
        print(self.header)
        print('\t\t       Spotify Music Downloader')
        print(f'\t\t\t   version {__version__}')
        print(f'\t\t\t  SMDC {CORE.VERSION}\n')

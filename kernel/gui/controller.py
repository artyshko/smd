 #
 # SMD GUI CONTROLLER
 #
import os
import sys
import imp
import types
import logging
from six import exec_
from flask import Flask, render_template, request, redirect, url_for

logging.basicConfig(
    level=logging.INFO,
    format=f'SMD_GUI %(asctime)s [ %(levelname)-2s ] (%(name)s) [%(funcName)s] %(message)s'
)
_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(logging.INFO)

MAIN_SERVER = Flask(__name__)

class IncludeManager(object):

    def __init__(self):

        self._logger = logging.getLogger("IM")

        self.apps = {}

    def __enter__(self):

        self._logger.info('Start including apps')

        from kernel.gui.apps import __init__ as apps
        __apps__ = { key:val for (key,val) in apps.__self__.__dict__.items() if type(val) is types.ModuleType}

        for app in __apps__:
            
            loaded_app = imp.load_source(app,__apps__[app].__file__)
            __flask__ = { key:val for (key,val) in loaded_app.__dict__.items() if type(val) is types.ModuleType}
            
            for _fl_ in __flask__:

                keys = __flask__[_fl_].__dict__.keys()
                self.apps[__flask__[_fl_].__dict__['__flask_app__']] = __flask__[_fl_]

        self._logger.info(f'{len(self.apps)} apps detected')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self._logger.warning('CLOSED')



class GUI():

    __slots__ = [
        'apps',
        '_logger'
    ]
    
    @staticmethod
    def init_apps(ima=None):

        GUI._logger = logging.getLogger("GUI")

        GUI.apps = {}

        for app in ima:

            GUI.apps[app] = ima[app]
            for rule in GUI.apps[app].app.url_map.iter_rules():
                if rule.endpoint == 'static': continue
                MAIN_SERVER.add_url_rule(str(rule), view_func=GUI.apps[app].__dict__[rule.endpoint])
        
        GUI._logger.info('Apps were loaded')

    @staticmethod
    def build_menu():

        _menu_items_ = {}

        for _ in GUI.apps:
            if GUI.apps[_].__visible__:
                _menu_items_[_] = GUI.apps[_] 
            else:
                 continue


    @staticmethod
    def runserver():

        MAIN_SERVER.run()

if __name__ == "__main__":

    

    with IncludeManager() as im:

        GUI.init_apps(im.apps)
    
   #GUI.runserver()
    

    


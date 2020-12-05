__point__ = 'GUI'

from kernel import controller
from kernel.smdc.core import CORE
from modules.addons import genius
from kernel.gui import controller as GC

class POINT():

    def __init__(self, args):
        pass

    def run(self):

        with GC.IncludeManager() as im:

            GC.GUI.init_apps(im.apps)
    
        GC.GUI.build_menu()

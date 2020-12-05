from kernel import controller
import sys

if __name__ == "__main__":

    point = controller.ConfigHandler.get_config('STARTPOINT')
    from points import __init__ as points
    __point__ = { key:val for (key,val) in points.__self__.__dict__.items() if key == point}
    __point__ = __point__[point] if __point__ else None
    __point__ = __point__(sys.argv) if __point__ else None
    __point__.run()

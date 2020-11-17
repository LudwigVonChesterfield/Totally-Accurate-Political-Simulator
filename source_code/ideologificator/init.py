import global_vars as gv

from .defines import *
from .helpers import get_max_axis_dist

def init(viewpoints):
	gv.IDEO_MAX_POS_DIST = get_max_axis_dist(len(viewpoints))
	gv.IDEO_MOD_MAX_DIST = gv.IDEO_MAX_POS_DIST * IDE_MOD_MAX_DIST_MULT

import os
import sys
import math
import copy
import random
import time
import yaml
from threading import Lock, Thread
from pyniryo import *
from poses import *
from odoo import *
import robots
from settings import *

def match_table_ref_to_robots(order: str):
    try:
        match order:
                case 'GR01':
                    return {ObjectShape.SQUARE, ObjectColor.GREEN}
                case 'GC01':
                    return {ObjectShape.CIRCLE, ObjectColor.GREEN}
                case 'RR01':
                    return {ObjectShape.SQUARE, ObjectColor.RED}
                case 'RC01':
                    return {ObjectShape.CIRCLE, ObjectColor.RED}
                case 'BR01':
                    return {ObjectShape.SQUARE, ObjectColor.BLUE}
                case 'BC01':
                    return {ObjectShape.CIRCLE, ObjectColor.BLUE}
    except:
        print("Input invalid or does not exist in database")


def execute_order_66(order: str):
    shape = match_table_ref_to_robots(order)[0]
    color = match_table_ref_to_robots(order)[1]

    return shape, color




                
         
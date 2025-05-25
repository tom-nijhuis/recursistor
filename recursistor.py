#!python3
# import sympy as sp
import random


class ResNet():
    SERIES, PARALLEL, SINGLE = 'sp1'

    def __init__(self, v = None) -> None:
        self.v = v
        self.net = []
        self.nettype = ResNet.SINGLE # SERIES, PARALLEL, or SINGLE
        pass

    def __add__(self, other): # Series addition
        if type(other) == set:
            return set(self + o for o in other if self.v != 0 and  o.v != 0) # Skip series with 0
        if self.v == 0 : return other # In series with 0
        if other.v == 0 : return self # In series with 0

        ret = ResNet(v = self.v + other.v)
        ret.net = [self,other]
        ret.nettype = ResNet.SERIES
        return ret.simplify_net()
    
    def __or__(self, other): # Parallel multiplication
        if type(other) == set:
            ret_set = set(self | o for o in other if self.v != 0 and  o.v != 0) # Skip parallel with 0
            return set(r for r in ret_set if r)
        if self.v == 0 or other.v == 0 : return ResNet(0) # In parallel with 0, return 0

        ret = ResNet(v = 1/(1/self.v + 1/other.v))
        ret.net = [self,other]
        ret.nettype = ResNet.PARALLEL
        return ret.simplify_net()
    
    def __mul__(self, other):
        return self | other
    
    def __repr__(self) -> str:
        return f"{self.v}Ω"
    
    def __format__(self, format_spec) -> str:
        return format(self.v, format_spec)+'Ω'

    def __lt__(self, other):
        try:
            if self.v == other.v: return self.deeplen < other.deeplen
            return self.v < other.v
        except TypeError:
            return True
    
    def __eq__(self, other):
        if isinstance(other, ResNet):
            return self.__hash__() == other.__hash__()
        return NotImplemented
    
    def __hash__(self):
        if self.nettype == ResNet.SINGLE:
            return self.v.__hash__()
        # Sum all the parts (note: sum is commutative, as is series/parllel connection)
        return sum([s.__hash__() for s in self.net]) + self.nettype.__hash__()
    
    def __len__(self):
        if self.nettype == ResNet.SINGLE: return 1
        return len(self.net)
    
    def subs(self, *kwargs):
        if self.nettype == ResNet.SINGLE:
            try:
                self.v = self.v.subs(*kwargs)
            except AttributeError: # Not a sympy object
                pass
        else:
            for r in self.net:
                r.subs(*kwargs)
        return self.simplify_net()
    
    @property
    def deeplen(self):
        if self.nettype == ResNet.SINGLE: return len(self)
        return sum(r.deeplen for r in self.net)

    def simplify_net(self, sort = False):
        if self.nettype == ResNet.SINGLE:
            return self
        newnet = []
        for r in self.net:
            r.simplify_net()
            if r.v == 0:
                if self.nettype == ResNet.PARALLEL:
                    self = ResNet(0)
                    return self
                if self.nettype == ResNet.SERIES:
                    continue
            if r.nettype == self.nettype:
                newnet += r.net
            else:
                newnet += [r]
        self.net = newnet
        if sort: self.net = sorted(self.net)
        return self
    
    # Drawing methods
    @property
    def width(self):
        if self.nettype == ResNet.SINGLE:   return len(f"{self}") + 2
        if self.nettype == ResNet.SERIES:   return sum(r.width for r in self.net)
        if self.nettype == ResNet.PARALLEL: return max(r.width for r in self.net) + 2

    @property
    def height(self):
        if self.nettype == ResNet.SINGLE:   return 1
        if self.nettype == ResNet.SERIES:   return max(r.height for r in self.net)
        if self.nettype == ResNet.PARALLEL: return sum(r.height for r in self.net)

    """
    Box

    ┳━┳
    ┣━┫
    ┃ ┃
    ┗━┛
    """

    def draw(self):
        return '\n'.join(self._draw()) 

    def _draw(self):
        ret_str = self.height*['']
        if self.nettype == ResNet.SINGLE:
            return [f"━{self}━"]
        if self.nettype == ResNet.PARALLEL:
            return self._draw_parallel(ret_str)
        if self.nettype == ResNet.SERIES:
            return self._draw_series(ret_str)
    
    def _draw_parallel(self, ret_str):
        if self.nettype != ResNet.PARALLEL:
            raise TypeError
        row_index = 0
        for part_ind,part in enumerate(self.net):
            hpad = self.width - part.width - 2
            hpadr = hpad //2      # padding right
            hpadl = hpad - hpadr # Padding left
            left, right = "┳┳" # Top connector
            for part_line_ind,part_line in enumerate(part._draw()):
                pad_char = " "
                if part_line_ind == 0: # Connector to new part at the bottom
                    pad_char = '━'
                    if part_ind>0: left, right = "┣┫"
                else:
                    left, right = "┃┃"
                if part_ind == len(self)-1:
                    if part_line_ind == 0:left, right = "┗┛"
                    else: left, right = "  "
                ret_str[row_index] = left + hpadl*pad_char + part_line + hpadr*pad_char + right 
                row_index += 1
        return ret_str
        
    def _draw_series(self, ret_str):
        if self.nettype != ResNet.SERIES:
            raise TypeError
        row_index = 0
        for part_ind, part in enumerate(self.net):
            part_str = part._draw()
            for row_index in range(self.height):
                if row_index >= part.height:
                    ret_str[row_index] += part.width * ' '
                else: 
                    ret_str[row_index] += part_str[row_index]
        return ret_str



def get_combinations(resistors):
    # Base case
    if len(resistors) == 1:
        resistor = resistors[0]
        return set([ResNet(0), resistor])
    
    # Recurse case
    ret_set = set()
    for i, resistor in enumerate(resistors):
        remaining_combos = get_combinations(resistors[:i] + resistors[i+1:])
        # Leave it out
        ret_set = ret_set.union(remaining_combos)
        # Serial with the rest
        ret_set = ret_set.union(resistor + remaining_combos)
        # Parallel with the rest:
        ret_set = ret_set.union(resistor | remaining_combos)

    return ret_set

def random_net(res_count = 5):
    if res_count == 1:
        return random.choice([ResNet(i) for i in range(1,5)])
    split = random.randint(1,res_count-1)
    A = random_net(split)
    B = random_net(res_count - split)
    if random.random() > .5:
        return A | B
    else: 
        return A + B


"""
    Main access
"""
if __name__ == "__main__":
    R = ResNet

    combos = sorted(get_combinations(2*[R(1)]+2*[R(3)]+[R(5), R(6)]))


    for r in combos:
        print(r.draw())
        print(f"Equivalent value: {r}")
        # if r.v > 0:
            # print("Current:",.5/r.v)
        print("\n")



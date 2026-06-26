''' For Optimal Page Replacement Algorithm logic '''

class OptimalRep:
    def __init__(self, ref_str, fcount):
        self.ref_str = ref_str
        self.fcount = fcount
    
    def run(self):
        steps = []
        frames = []
        hits  = 0
        faults = 0
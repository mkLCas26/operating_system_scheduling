''' For FIFO Page Replacement Algorithm logic '''

class FIFORep:
    def __init__(self, ref_str, fcount):
        self.ref_str = ref_str
        self.fcount = fcount
        
    def run(self):
        queue = []
        steps = []
        frames =[]
        hits = 0
        faults = 0
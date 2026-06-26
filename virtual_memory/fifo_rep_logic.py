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
        
        for page in self.ref_str:
            if page in frames:
                hits += 1
                steps.append({
                    "page": page,
                    "frames": frames.copy(),
                    "status": "HIT"
                })
                
            else:
                faults += 1
                
                if len(frames) < self.fcount:
                    frames.append(page)
                    queue.append(page)
                    
                else:
                    oldest_page = queue.pop(0)
                    target = frames.index(oldest_page)
                    frames[target] = page
                    queue.append(page)
                    
                
                steps.append({
                    "page": page,
                    "frames": frames.copy(),
                    "status": "FAULT"
                })
        
        return{
            "fault_total": faults,
            "hit_total": hits,
            "steps": steps
        }
                
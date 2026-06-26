''' For Most Frequently Used Page Replacement Algorithm logic '''

class MFURep:
    def __init__(self, ref_str, fcount):
        self.ref_str = ref_str
        self.fcount = fcount
    
    def run(self):
        steps = []
        frames = []
        hits  = 0
        faults = 0
        count = {}
        fifo_fallback = {}
        
        for i, page in enumerate(self.ref_str):
            count[page] = count.get(page, 0) + 1
            
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
                    fifo_fallback[page] = i
                    
                else:
                    max_count = max(count[f] for f in frames)
                    check = [f for f in frames if count[f] == max_count]
                    
                    target = min(check, key=lambda c: fifo_fallback[c])
                    
                    target = frames.index(target)
                    frames[target] = page
                    fifo_fallback[page] = i
                
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
                 
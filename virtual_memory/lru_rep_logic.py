''' For Least Recently Used Page Replacement Algorithm logic '''

class LRURep:
    def __init__(self, ref_str, fcount):
        self.ref_str = ref_str
        self.fcount = fcount
    
    def run(self):
        steps = []
        frames = []
        hits  = 0
        faults = 0
        
        for i, page in enumerate(self.ref_str):
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
                
                else:
                    target = -1
                    least_recent = i
                    
                    for frame_pos, frame_page in enumerate(frames):
                        recently_used = len(self.ref_str[:i]) - 1 - self.ref_str[:i][::-1].index(frame_page)
                        
                        if recently_used < least_recent:
                            least_recent = recently_used
                            target = frame_pos
                    
                    frames[target] = page
                
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
                 
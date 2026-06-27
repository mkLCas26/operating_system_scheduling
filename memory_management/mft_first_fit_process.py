"""
MFT (Multi-partition Fixed Table) Memory Allocation Engine
Implements First-Fit memory allocation strategy with OOP principles
"""


class MemoryPartition:
    """Represents a memory partition in the MFT system"""
    
    def __init__(self, partition_id, start, size):
        self.partition_id = partition_id
        self.start = start
        self.end = start + size
        self.size = size
        self.assigned_job = None
        self.job_size = 0
        self.internal_frag = 0
        self.type = "standard"
    
    def is_available(self):
        """Check if partition is available for allocation"""
        return self.assigned_job is None
    
    def can_fit_job(self, job_size):
        """Check if a job can fit in this partition"""
        return self.is_available() and self.size >= job_size
    
    def allocate_job(self, job_id, job_size):
        """Allocate a job to this partition"""
        if not self.can_fit_job(job_size):
            return False
        
        self.assigned_job = job_id
        self.job_size = job_size
        self.internal_frag = self.size - job_size
        return True
    
    def deallocate_job(self):
        """Deallocate a job from this partition"""
        self.assigned_job = None
        self.job_size = 0
        self.internal_frag = 0
    
    def to_dict(self):
        """Convert partition to dictionary representation"""
        return {
            "id": self.partition_id,
            "start": self.start,
            "end": self.end,
            "size": self.size,
            "assigned_job": self.assigned_job,
            "job_size": self.job_size,
            "internal_frag": self.internal_frag,
            "type": self.type
        }


class Process:
    """Represents a process/job in the system"""
    
    def __init__(self, job_id, job_size):
        self.job_id = job_id
        self.job_size = job_size
        self.allocated = False
        self.allocated_partition = None
    
    def is_valid(self):
        """Check if process has valid size"""
        return self.job_size > 0
    
    def to_dict(self):
        """Convert process to dictionary representation"""
        return {
            "job_id": self.job_id,
            "job_size": self.job_size,
            "allocated": self.allocated,
            "allocated_partition": self.allocated_partition
        }


class MFTProcessEngine:
    """
    MFT Memory Allocation Engine using First-Fit strategy
    Manages memory partitions and process allocation
    """
    
    def __init__(self, total_memory):
        """Initialize the engine with total memory size"""
        self.total_memory = total_memory
        self.partitions = []
        self.allocated_jobs = []
        self.waiting_jobs = []
        self.allocation_history = []
    
    def setup_partitions(self, partition_sizes):
        """Setup memory partitions based on provided sizes"""
        self.partitions = []
        current_address = 0
        
        # Validate total partition size
        total_parts_sum = sum(partition_sizes)
        if total_parts_sum > self.total_memory:
            raise ValueError(
                f"Sum of partitions ({total_parts_sum}k) exceeds Total Memory Size ({self.total_memory}k)!"
            )
        
        # Create standard partitions
        for idx, size in enumerate(partition_sizes):
            if size > 0:
                partition = MemoryPartition(
                    f"Partition {idx + 1}",
                    current_address,
                    size
                )
                self.partitions.append(partition)
                current_address += size
        
        # Create unused space partition if applicable
        unpartitioned_rem = self.total_memory - total_parts_sum
        if unpartitioned_rem > 0:
            unused_partition = MemoryPartition(
                "Unused Space",
                current_address,
                unpartitioned_rem
            )
            unused_partition.type = "unpartitioned"
            self.partitions.append(unused_partition)
        
        return len(self.partitions)
    
    def allocate_process(self, job_id, job_size):
        """Allocate a process using First-Fit strategy"""
        if job_size <= 0:
            return False, f"Invalid job size for {job_id}"
        
        # Find first available partition that fits
        for partition in self.partitions:
            if partition.type == "standard" and partition.can_fit_job(job_size):
                success = partition.allocate_job(job_id, job_size)
                if success:
                    self.allocated_jobs.append(job_id)
                    self.allocation_history.append({
                        "job_id": job_id,
                        "job_size": job_size,
                        "partition": partition.partition_id,
                        "internal_frag": partition.internal_frag,
                        "status": "ALLOCATED"
                    })
                    return True, f"Allocated {job_id} ({job_size}k) in {partition.partition_id}"
        
        # No suitable partition found
        self.waiting_jobs.append(job_id)
        self.allocation_history.append({
            "job_id": job_id,
            "job_size": job_size,
            "partition": None,
            "internal_frag": 0,
            "status": "WAITING"
        })
        return False, f"Cannot allocate {job_id} ({job_size}k) - No suitable free block"
    
    def calculate_metrics(self):
        """Calculate memory utilization metrics"""
        total_internal_frag = sum(
            p.internal_frag for p in self.partitions if p.type == "standard"
        )
        total_used_ram = sum(
            p.job_size for p in self.partitions if p.assigned_job is not None
        )
        mem_utilization_pct = (total_used_ram / self.total_memory * 100) if self.total_memory > 0 else 0
        
        return {
            "total_internal_frag": total_internal_frag,
            "total_used_ram": total_used_ram,
            "mem_utilization_pct": mem_utilization_pct
        }
    
    def generate_diary_report(self):
        """Generate allocation diary report"""
        report = "📝 --- CHRONICLE ALLOCATION DIARY (FIRST-FIT STRATEGY) ---\n\n"
        
        for entry in self.allocation_history:
            if entry["status"] == "ALLOCATED":
                report += (
                    f"🟢 [ALLOCATED] -> {entry['job_id']} ({entry['job_size']}k) "
                    f"resides inside {entry['partition']}. "
                    f"(Internal Frag: {entry['internal_frag']}k)\n"
                )
            else:
                report += (
                    f"🔴 [WAITING]   -> {entry['job_id']} ({entry['job_size']}k) "
                    f"cannot be allocated. (Walang kasya na free block)\n"
                )
        
        metrics = self.calculate_metrics()
        report += (
            f"\n💡 SUMMARY ANALYSIS:\n"
            f"Total Internal Frag: {metrics['total_internal_frag']}k | "
            f"Global RAM Utilization: {metrics['mem_utilization_pct']:.2f}%"
        )
        
        return report
    
    def reset(self):
        """Reset engine state"""
        self.partitions = []
        self.allocated_jobs = []
        self.waiting_jobs = []
        self.allocation_history = []
    
    @staticmethod
    def calculate_allocation(total_mem_limit, part_sizes, process_sizes, strategy="first"):
        """
        Static method for backward compatibility with existing GUI
        Performs complete allocation calculation
        """
        # Validation
        if total_mem_limit <= 0 or any(p <= 0 for p in part_sizes) or any(j < 0 for j in process_sizes.values()):
            raise ValueError("Bawal ang negative value o zero sa memory configuration fields!")
        
        # Initialize engine
        engine = MFTProcessEngine(total_mem_limit)
        engine.setup_partitions(part_sizes)
        
        # Allocate processes
        for job_id, job_size in process_sizes.items():
            if job_size > 0:
                engine.allocate_process(job_id, job_size)
        
        # Calculate metrics
        metrics = engine.calculate_metrics()
        total_parts_sum = sum(part_sizes)
        
        # Return result in GUI-compatible format
        return {
            "partitions": [p.to_dict() for p in engine.partitions],
            "allocated_jobs": engine.allocated_jobs,
            "waiting_jobs": engine.waiting_jobs,
            "total_internal_frag": metrics["total_internal_frag"],
            "mem_utilization_pct": metrics["mem_utilization_pct"],
            "diary_report": engine.generate_diary_report(),
            "total_parts_sum": total_parts_sum
        }

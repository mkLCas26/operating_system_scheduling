from collections import deque
from enum import Enum
from datetime import datetime


class CPUSchedulingAlgorithm(Enum):
    FCFS = "fcfs"
    SJF = "sjf"
    PRIORITY = "priority"
    ROUND_ROBIN = "round_robin"


class AllocationStrategy(Enum):
    FIRST_FIT = "first"
    BEST_FIT = "best"
    WORST_FIT = "worst"


class Process:
    def __init__(self, pid, arrival_time, burst_time, memory_size, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.memory_size = memory_size
        self.priority = priority
        self.allocated = False
        self.start_time = None
        self.end_time = None
        self.allocated_address = None
        self.allocated_memory_block = None


class MemoryBlock:
    def __init__(self, block_id, start_address, size, is_free=True):
        self.block_id = block_id
        self.start_address = start_address
        self.end_address = start_address + size
        self.size = size
        self.is_free = is_free
        self.allocated_process = None
        self.allocated_memory = 0
        self.internal_fragmentation = 0
        self.allocated_time = None


class MVTSimulator:
    def __init__(self, total_memory, cpu_scheduling="fcfs", allocation_strategy="first", enable_compaction=False):
        self.total_memory = total_memory
        self.cpu_scheduling = cpu_scheduling.lower()
        self.allocation_strategy = allocation_strategy.lower()
        self.enable_compaction = enable_compaction
        
        self.memory_blocks = []
        self.processes = []
        self.completed_processes = []
        self.waiting_queue = deque()
        self.execution_log = []
        self.current_time = 0
        self.ready_queue = deque()
        self.running_process = None
        self.context_switches = 0
        self.time_quantum = 4  # For Round Robin
        self.time_quantum_remaining = self.time_quantum
        
        # Initialize memory as one free block
        self._initialize_memory()
    
    def _initialize_memory(self):
        """Initialize memory as a single free block"""
        self.memory_blocks = [
            MemoryBlock(f"Block-0", 0, self.total_memory, is_free=True)
        ]
        self.log_event(f"Memory initialized: {self.total_memory}KB total")
    
    def add_process(self, pid, arrival_time, burst_time, memory_size, priority=0):
        """Add a process to the system"""
        process = Process(pid, arrival_time, burst_time, memory_size, priority)
        self.processes.append(process)
        self.log_event(f"Process {pid} added: arrival={arrival_time}, burst={burst_time}, memory={memory_size}KB, priority={priority}")
    
    def log_event(self, message):
        """Log an event"""
        timestamp = f"[T={self.current_time}]"
        self.execution_log.append(f"{timestamp} {message}")
    
    def _get_free_blocks(self):
        """Get all free memory blocks"""
        return [b for b in self.memory_blocks if b.is_free]
    
    def _try_allocate_process(self, process):
        """Try to allocate memory to a process using the chosen strategy"""
        if process.memory_size > self.total_memory:
            self.log_event(f"❌ Process {process.pid} cannot be allocated (exceeds total memory)")
            return False
        
        free_blocks = self._get_free_blocks()
        suitable_block = None
        
        if self.allocation_strategy == "first":
            # First Fit: Use first block that fits
            for block in free_blocks:
                if block.size >= process.memory_size:
                    suitable_block = block
                    break
        
        elif self.allocation_strategy == "best":
            # Best Fit: Use smallest block that fits
            suitable_block = None
            for block in free_blocks:
                if block.size >= process.memory_size:
                    if suitable_block is None or block.size < suitable_block.size:
                        suitable_block = block
        
        elif self.allocation_strategy == "worst":
            # Worst Fit: Use largest block that fits
            suitable_block = None
            for block in free_blocks:
                if block.size >= process.memory_size:
                    if suitable_block is None or block.size > suitable_block.size:
                        suitable_block = block
        
        if suitable_block:
            # Allocate process to this block
            internal_frag = suitable_block.size - process.memory_size
            
            # Split block if necessary
            if internal_frag > 0:
                # Create new free block from remaining space
                new_block = MemoryBlock(
                    f"Block-{len(self.memory_blocks)}",
                    suitable_block.start_address + process.memory_size,
                    internal_frag,
                    is_free=True
                )
                self.memory_blocks.append(new_block)
            
            # Mark current block as allocated
            suitable_block.is_free = False
            suitable_block.size = process.memory_size
            suitable_block.end_address = suitable_block.start_address + process.memory_size
            suitable_block.allocated_process = process.pid
            suitable_block.allocated_memory = process.memory_size
            suitable_block.internal_fragmentation = internal_frag
            suitable_block.allocated_time = self.current_time
            
            process.allocated = True
            process.allocated_address = suitable_block.start_address
            process.allocated_memory_block = suitable_block
            
            self.log_event(f"✅ Process {process.pid} allocated at {suitable_block.start_address}KB "
                          f"({process.memory_size}KB), internal frag: {internal_frag}KB")
            return True
        else:
            # Cannot allocate - check if compaction would help
            if self.enable_compaction:
                self._compact_memory()
                return self._try_allocate_process(process)
            else:
                self.log_event(f"⏳ Process {process.pid} waiting for memory (no suitable block)")
                return False
    
    def _compact_memory(self):
        """Compact memory by moving allocated blocks together"""
        self.log_event("🔄 Compacting memory...")
        
        allocated_blocks = [(b, b.allocated_time) for b in self.memory_blocks if not b.is_free]
        allocated_blocks.sort(key=lambda x: x[1] if x[1] else float('inf'))
        
        current_address = 0
        for block, _ in allocated_blocks:
            block.start_address = current_address
            block.end_address = current_address + block.allocated_memory
            current_address += block.allocated_memory
        
        # Create single free block at end
        free_size = self.total_memory - current_address
        self.memory_blocks = [block for block, _ in allocated_blocks]
        self.memory_blocks.append(MemoryBlock(f"Block-Free", current_address, free_size, is_free=True))
        
        self.log_event(f"✅ Memory compacted, free space: {free_size}KB at {current_address}KB")
    
    def _get_next_process_to_run(self):
        """Determine next process to run based on CPU scheduling algorithm"""
        if not self.ready_queue:
            return None
        
        if self.cpu_scheduling == "fcfs":
            return self.ready_queue.popleft()
        
        elif self.cpu_scheduling == "sjf":
            # Shortest Job First
            process = min(self.ready_queue, key=lambda p: p.remaining_time)
            self.ready_queue.remove(process)
            return process
        
        elif self.cpu_scheduling == "priority":
            # Priority scheduling (lower number = higher priority)
            process = min(self.ready_queue, key=lambda p: p.priority)
            self.ready_queue.remove(process)
            return process
        
        elif self.cpu_scheduling == "round_robin":
            return self.ready_queue.popleft()
        
        return None
    
    def _deallocate_process(self, process):
        """Deallocate memory from a process"""
        if process.allocated_memory_block:
            block = process.allocated_memory_block
            block.is_free = True
            block.allocated_process = None
            block.allocated_memory = 0
            block.internal_fragmentation = 0
            block.allocated_time = None
        
        self.log_event(f"🗑️  Process {process.pid} deallocated from memory")
        
        # Try to merge adjacent free blocks
        self._merge_free_blocks()
    
    def _merge_free_blocks(self):
        """Merge adjacent free blocks"""
        self.memory_blocks.sort(key=lambda b: b.start_address)
        
        merged = []
        for block in self.memory_blocks:
            if merged and merged[-1].is_free and block.is_free:
                merged[-1].size += block.size
                merged[-1].end_address = merged[-1].start_address + merged[-1].size
            else:
                merged.append(block)
        
        self.memory_blocks = merged
    
    def simulate(self, time_limit=100):
        """Run the MVT simulation"""
        self.log_event(f"Starting MVT simulation with {self.cpu_scheduling.upper()} scheduling "
                      f"and {self.allocation_strategy.upper()} allocation")
        
        time_step = 0
        
        while time_step <= time_limit:
            self.current_time = time_step
            
            # Check for arriving processes
            for process in self.processes:
                if process.arrival_time == time_step and process not in self.ready_queue and process not in self.completed_processes and not process.allocated:
                    self.ready_queue.append(process)
                    self.log_event(f"📥 Process {process.pid} arrived")
            
            # Try to allocate waiting processes
            processes_to_allocate = [p for p in self.ready_queue if not p.allocated]
            for process in processes_to_allocate:
                if self._try_allocate_process(process):
                    processes_to_allocate.remove(process)
            
            # Handle CPU execution
            if self.running_process and self.running_process.remaining_time > 0:
                self.running_process.remaining_time -= 1
                self.time_quantum_remaining -= 1
                
                if self.running_process.remaining_time == 0:
                    self.running_process.end_time = time_step
                    self.log_event(f"✅ Process {self.running_process.pid} completed")
                    self._deallocate_process(self.running_process)
                    self.completed_processes.append(self.running_process)
                    self.running_process = None
                    self.time_quantum_remaining = self.time_quantum
                
                elif self.cpu_scheduling == "round_robin" and self.time_quantum_remaining == 0:
                    self.log_event(f"⏱️  Time quantum expired for Process {self.running_process.pid}")
                    self.running_process.start_time = None  # Reset for next execution
                    self.ready_queue.append(self.running_process)
                    self.running_process = None
                    self.time_quantum_remaining = self.time_quantum
                    self.context_switches += 1
            
            # Get next process to run
            if not self.running_process and self.ready_queue:
                allocated_processes = [p for p in self.ready_queue if p.allocated]
                if allocated_processes:
                    self.ready_queue = deque(allocated_processes)
                    self.running_process = self._get_next_process_to_run()
                    if self.running_process:
                        if not self.running_process.start_time:
                            self.running_process.start_time = time_step
                        self.log_event(f"🚀 Process {self.running_process.pid} started execution")
            
            # Check if all processes are done
            if len(self.completed_processes) == len(self.processes):
                self.log_event("🏁 All processes completed")
                break
            
            time_step += 1
        
        return self._generate_report()
    
    def _generate_report(self):
        """Generate simulation report"""
        total_turnaround_time = 0
        total_waiting_time = 0
        
        for process in self.completed_processes:
            if process.end_time and process.arrival_time:
                turnaround = process.end_time - process.arrival_time
                waiting = turnaround - process.burst_time
                total_turnaround_time += turnaround
                total_waiting_time += waiting
        
        avg_turnaround = total_turnaround_time / len(self.completed_processes) if self.completed_processes else 0
        avg_waiting = total_waiting_time / len(self.completed_processes) if self.completed_processes else 0
        
        total_internal_frag = sum(b.internal_fragmentation for b in self.memory_blocks if not b.is_free)
        external_frag = sum(b.size for b in self.memory_blocks if b.is_free)
        
        report = {
            "scheduling_algorithm": self.cpu_scheduling.upper(),
            "allocation_strategy": self.allocation_strategy.upper(),
            "compaction_enabled": self.enable_compaction,
            "total_memory": self.total_memory,
            "processes_completed": len(self.completed_processes),
            "avg_turnaround_time": round(avg_turnaround, 2),
            "avg_waiting_time": round(avg_waiting, 2),
            "context_switches": self.context_switches,
            "total_internal_fragmentation": total_internal_frag,
            "total_external_fragmentation": external_frag,
            "execution_log": self.execution_log,
            "memory_blocks": [
                {
                    "block_id": b.block_id,
                    "start": b.start_address,
                    "end": b.end_address,
                    "size": b.size,
                    "allocated_process": b.allocated_process,
                    "is_free": b.is_free,
                    "internal_frag": b.internal_fragmentation
                }
                for b in self.memory_blocks
            ],
            "completed_processes": [
                {
                    "pid": p.pid,
                    "arrival_time": p.arrival_time,
                    "burst_time": p.burst_time,
                    "start_time": p.start_time,
                    "end_time": p.end_time,
                    "turnaround_time": (p.end_time - p.arrival_time) if p.end_time else None,
                    "waiting_time": (p.start_time - p.arrival_time) if p.start_time else None,
                }
                for p in self.completed_processes
            ]
        }
        
        return report

class MFTWorstFit:
    @staticmethod
    def calculate_allocation(total_mem_limit, part_sizes, process_sizes, strategy="worst"):
  
        supported_strategies = {"first", "best", "worst"}
        if strategy not in supported_strategies:
            raise ValueError(f"Unsupported allocation strategy: {strategy}")

        if total_mem_limit <= 0 or any(p <= 0 for p in part_sizes) or any(j < 0 for j in process_sizes.values()):
            raise ValueError("Bawal ang negative value o zero sa memory configuration fields!")

        total_parts_sum = sum(part_sizes)
        if total_parts_sum > total_mem_limit:
            raise ValueError(f"Ang sum ng partitions ({total_parts_sum}k) ay lumagpas sa Total Memory Size ({total_mem_limit}k)!")

        partitions = []
        current_address = 0
        for i, size in enumerate(part_sizes):
            partitions.append({
                "id": f"Partition {i+1}",
                "start": current_address,
                "end": current_address + size,
                "size": size,
                "assigned_job": None,
                "job_size": 0,
                "internal_frag": 0,
                "type": "standard"
            })
            current_address += size

        unpartitioned_rem = total_mem_limit - total_parts_sum
        if unpartitioned_rem > 0:
            partitions.append({
                "id": "Unused Space",
                "start": current_address,
                "end": total_mem_limit,
                "size": unpartitioned_rem,
                "assigned_job": None,
                "job_size": 0,
                "internal_frag": 0,
                "type": "unpartitioned"
            })

        allocated_jobs_list = []
        waiting_jobs_list = []
        total_internal_frag = 0
        total_active_used_ram = 0

        diary_report = "📝 --- CHRONICLE ALLOCATION DIARY (WORST-FIT STRATEGY) ---\n\n"

        for job_id, job_size in process_sizes.items():
            if job_size == 0:
                continue 
                
            allocated = False
            worst_partition = None
            max_free_space = -1
            
            # Find partition with most free space (worst fit)
            for p in partitions:
                if p["type"] == "standard" and p["assigned_job"] is None and p["size"] >= job_size:
                    free_space = p["size"] - job_size
                    if free_space > max_free_space:
                        max_free_space = free_space
                        worst_partition = p
            
            if worst_partition is not None:
                worst_partition["assigned_job"] = job_id
                worst_partition["job_size"] = job_size
                worst_partition["internal_frag"] = max_free_space
                
                total_internal_frag += max_free_space
                total_active_used_ram += job_size
                allocated_jobs_list.append(job_id)
                
                diary_report += f"🟢 [ALLOCATED] -> {job_id} ({job_size}k) resides inside {worst_partition['id']}. (Internal Frag: {max_free_space}k)\n"
                allocated = True
            
            if not allocated:
                waiting_jobs_list.append(job_id)
                diary_report += f"🔴 [WAITING]   -> {job_id} ({job_size}k) cannot be allocated. (Walang kasya na free block)\n"

        mem_utilization_pct = (total_active_used_ram / total_mem_limit) * 100 if total_mem_limit > 0 else 0
        diary_report += f"\n💡 SUMMARY ANALYSIS:\nTotal Internal Frag: {total_internal_frag}k | Global RAM Utilization: {mem_utilization_pct:.2f}%"

        return {
            "partitions": partitions,
            "allocated_jobs": allocated_jobs_list,
            "waiting_jobs": waiting_jobs_list,
            "total_internal_frag": total_internal_frag,
            "mem_utilization_pct": mem_utilization_pct,
            "diary_report": diary_report,
            "total_parts_sum": total_parts_sum
        }

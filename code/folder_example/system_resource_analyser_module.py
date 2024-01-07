import psutil
from datetime import datetime

def get_cpu_usage():
    cpu_info = psutil.cpu_percent(interval=1)
    
    print(f"-- CPU Usage at {datetime.now()}: {cpu_info}%")
    
    return cpu_info

def get_memory_usage():
    memory = psutil.virtual_memory()
    
    memory_info = {
        'total': memory.total,
        'available': memory.available,
        'used': memory.used,
        'percent': memory.percent
    }
    
    print(f"-- Memory Usage at {datetime.now()}:")
    print("Total: {} MB".format(memory_info['total'] / (1024 * 1024)))
    print("Used: {} MB".format(memory_info['used'] / (1024 * 1024)))
    print("Free: {} MB".format(memory_info['available'] / (1024 * 1024)))
    print("Usage Percentage: {}%".format(memory_info['percent']))
    
    return memory_info

def get_disk_usage():
    disk = psutil.disk_usage('/')
    
    disk_info = {
        'total': disk.total,
        'used': disk.used,
        'free': disk.free,
        'percent': disk.percent
    }
    
    print(f"-- Disk Usage at {datetime.now()}:")
    print("Total: {} GB".format(disk_info['total'] / (1024 * 1024 * 1024)))
    print("Used: {} GB".format(disk_info['used'] / (1024 * 1024 * 1024)))
    print("Free: {} GB".format(disk_info['free'] / (1024 * 1024 * 1024)))
    print("Usage Percentage: {}%".format(disk_info['percent']))
    
    return disk_info

"""def main():
    cpu_info = get_cpu_usage()
    
    memory_info = get_memory_usage()

    disk_info = get_disk_usage()"""
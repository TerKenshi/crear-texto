#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Pmw
import platform
import threading
import psutil
from datetime import datetime

ventana = Pmw.initialise(fontScheme = 'pmw1')
ventana.title("SYSTEM/HARDWARE INFO")

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def clear():
    display.clear()
    display.appendtext("USE THE BUTTONS TO SELECT THE INFORMATION.\n\n")

def network():
    display.appendtext(("="*45)+"Network Information"+(("=")*45)+"\n")
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            display.appendtext(f"=== Interface: {interface_name} ===\n")
            if str(address.family) == 'AddressFamily.AF_INET':
                display.appendtext(f"  IP Address: {address.address}\n")
                display.appendtext(f"  Netmask: {address.netmask}\n")
                display.appendtext(f"  Broadcast IP: {address.broadcast}\n")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                display.appendtext(f"  MAC Address: {address.address}\n")
                display.appendtext(f"  Netmask: {address.netmask}\n")
                display.appendtext(f"  Broadcast MAC: {address.broadcast}\n")
    net_io = psutil.net_io_counters()
    display.appendtext(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}\n")
    display.appendtext(f"Total Bytes Received: {get_size(net_io.bytes_recv)}\n")
    display.appendtext("="*109)

def disk():
    display.appendtext(("="*46)+"Disk Information"+(("=")*46)+"\n")
    display.appendtext("Partitions and Usage:\n")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        display.appendtext(f"=== Device: {partition.device} ===\n")
        display.appendtext(f" Mountpoint: {partition.mountpoint}\n")
        display.appendtext(f" File system type: {partition.fstype}\n")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        display.appendtext(f" Total Size: {get_size(partition_usage.total)}\n")
        display.appendtext(f" Used: {get_size(partition_usage.used)}\n")
        display.appendtext(f" Free: {get_size(partition_usage.free)}\n")
        display.appendtext(f" Percentage: {partition_usage.percent}%\n")
    disk_io = psutil.disk_io_counters()
    display.appendtext(f" Total read: {get_size(disk_io.read_bytes)}\n")
    display.appendtext(f" Total write: {get_size(disk_io.write_bytes)}\n")
    display.appendtext("="*108)

def memory():
    display.appendtext(("="*45)+"Memory Information"+(("=")*45)+"\n")
    svmem = psutil.virtual_memory()
    display.appendtext(f"Total: {get_size(svmem.total)}\n")
    display.appendtext(f"Available: {get_size(svmem.available)}\n")
    display.appendtext(f"Used: {get_size(svmem.used)}\n")
    display.appendtext(f"Percentage: {svmem.percent}%\n")
    display.appendtext(("="*20)+"SWAP"+("="*20)+"\n")
    swap = psutil.swap_memory()
    display.appendtext(f"Total: {get_size(swap.total)}\n")
    display.appendtext(f"Free: {get_size(swap.free)}\n")
    display.appendtext(f"Used: {get_size(swap.used)}\n")
    display.appendtext(f"Percentage: {swap.percent}%\n")
    display.appendtext("="*108)

def system():
    display.appendtext(("="*45)+"System Information"+(("=")*45)+"\n")
    uname = platform.uname()
    display.appendtext(f"System: {uname.system}\n")
    display.appendtext(f"Node Name: {uname.node}\n")
    display.appendtext(f"Release: {uname.release}\n")
    display.appendtext(f"Version: {uname.version}\n")
    display.appendtext(f"Machine: {uname.machine}\n")
    display.appendtext(f"Processor: {uname.processor}\n")
    display.appendtext("="*108)
    
def cpu():
    display.appendtext(("="*47)+"CPU Information"+(("=")*47)+"\n")
    display.appendtext(("Physical cores: "+str(psutil.cpu_count(logical=False))))
    display.appendtext("\n")
    display.appendtext(("Total cores: "+str(psutil.cpu_count(logical=True))))
    display.appendtext("\n")
    cpufreq = psutil.cpu_freq()
    display.appendtext(f"Max Frequency: {cpufreq.max:.2f}Mhz\n")
    display.appendtext(f"Min Frequency: {cpufreq.min:.2f}Mhz\n")
    display.appendtext(f"Current Frequency: {cpufreq.current:.2f}Mhz\n")
    display.appendtext("CPU Usage Per Core:\n")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        display.appendtext(f"Core {i}: {percentage}%\n")
    display.appendtext(f"Total CPU Usage: {psutil.cpu_percent()}%\n")
    display.appendtext("="*109)
    
def inicia(index):
    infos={0:system,1:cpu,2:memory,3:disk,4:network,5:imprimir}
    t=threading.Thread(target=infos[index])
    t.start()
def imprimir():
    ar=open("T:\datospc.txt","+r")
    
    ar.writelines([("="*45)+"System Information"+(("=")*45)+"\n"])
    uname = platform.uname()
    ar.write(f"System: {uname.system}\n")
    ar.write(f"Node Name: {uname.node}\n")
    ar.write(f"Release: {uname.release}\n")
    ar.write(f"Version: {uname.version}\n")
    ar.write(f"Machine: {uname.machine}\n")
    ar.write(f"Processor: {uname.processor}\n")
    ar.write("="*108)

    ar.writelines(("="*47)+"CPU Information"+(("=")*47)+"\n")
    ar.write(("Physical cores: "+str(psutil.cpu_count(logical=False))))
    ar.write("\n")
    ar.write(("Total cores: "+str(psutil.cpu_count(logical=True))))
    ar.write("\n")
    cpufreq = psutil.cpu_freq()
    ar.write(f"Max Frequency: {cpufreq.max:.2f}Mhz\n")
    ar.write(f"Min Frequency: {cpufreq.min:.2f}Mhz\n")
    ar.write(f"Current Frequency: {cpufreq.current:.2f}Mhz\n")
    ar.write("CPU Usage Per Core:\n")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        ar.write(f"Core {i}: {percentage}%\n")
    ar.write(f"Total CPU Usage: {psutil.cpu_percent()}%\n")
    ar.write("="*109)

    ar.writelines(("="*45)+"Memory Information"+(("=")*45)+"\n")
    svmem = psutil.virtual_memory()
    ar.write(f"Total: {get_size(svmem.total)}\n")
    ar.write(f"Available: {get_size(svmem.available)}\n")
    ar.write(f"Used: {get_size(svmem.used)}\n")
    ar.write(f"Percentage: {svmem.percent}%\n")
    ar.write(("="*20)+"SWAP"+("="*20)+"\n")
    swap = psutil.swap_memory()
    ar.write(f"Total: {get_size(swap.total)}\n")
    ar.write(f"Free: {get_size(swap.free)}\n")
    ar.write(f"Used: {get_size(swap.used)}\n")
    ar.write(f"Percentage: {swap.percent}%\n")
    ar.write("="*108)


    ar.writelines(("="*46)+"Disk Information"+(("=")*46)+"\n")
    ar.write("Partitions and Usage:\n")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        ar.write(f"=== Device: {partition.device} ===\n")
        ar.write(f" Mountpoint: {partition.mountpoint}\n")
        ar.write(f" File system type: {partition.fstype}\n")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        ar.write(f" Total Size: {get_size(partition_usage.total)}\n")
        ar.write(f" Used: {get_size(partition_usage.used)}\n")
        ar.write(f" Free: {get_size(partition_usage.free)}\n")
        ar.write(f" Percentage: {partition_usage.percent}%\n")
    disk_io = psutil.disk_io_counters()
    ar.write(f" Total read: {get_size(disk_io.read_bytes)}\n")
    ar.write(f" Total write: {get_size(disk_io.write_bytes)}\n")
    ar.write("="*108)
         
#PANTALLA
display = Pmw.ScrolledText(ventana, hscrollmode='none',
                      vscrollmode='dynamic', hull_relief='sunken',
                      hull_background='gray20', hull_borderwidth=10,
                      text_background='black', text_width=109,
                      text_foreground='green', text_height=39,
                      text_padx=10, text_pady=10, text_relief='groove',
                      text_font=('Fixedsys', 10))
display.pack(padx=0,pady=0)

#BOTONES
botones = Pmw.ButtonBox(ventana)
botones.pack(fill='both', expand=1, padx=1, pady=1)

botones.add('System Info',command=lambda:inicia(0),width=15,bg='light green')
botones.add('CPU Info',command=lambda:inicia(1),bg='light green')
botones.add('Memory Info',command=lambda:inicia(2),bg='light green')
botones.add('Disk Info',command=lambda:inicia(3),bg='light green')
botones.add('Network Info',command=lambda:inicia(4),bg='light green')
botones.add('CLEAR',command=clear,bg='light blue')
botones.add('imprimir',command=lambda:inicia(5),bg='light green')
botones.alignbuttons()

clear()

ventana.mainloop()

    

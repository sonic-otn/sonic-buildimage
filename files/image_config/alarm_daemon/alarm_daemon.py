#!/usr/bin/python3
import subprocess
import threading
import psutil
from otn_pmon.alarm import Alarm
import otn_pmon.db as db
from sonic_py_common.logger import Logger

LOG = Logger("ALARMD", Logger.LOG_FACILITY_USER, Logger.LOG_OPTION_NDELAY)
LOG.set_min_log_priority_info()

class CPUMonitor(threading.Thread) :
    CPU_MEMORY_USAGE_THRESH = 80

    def __init__(self, sample_times = 20, interval_secs = 1) :
        threading.Thread.__init__(self)
        self.sample_times = sample_times
        self.interval_secs = interval_secs
        self.cpu_stats = []
    
    def _log(self) :
        top_info = subprocess.Popen(f"top -b -n 1 | head -n 17", shell=True, stdout=subprocess.PIPE)
        out, err = top_info.communicate()
        if err :
            return
        out_info = out.decode('unicode-escape')
        LOG.log_info(f"cpu top details :\n {out_info}")

    def cpu_high(self) :
        count = 0
        for percent in self.cpu_stats :
            if percent > CPUMonitor.CPU_MEMORY_USAGE_THRESH :
                count = count + 1

        sample_size = int(self.sample_times / self.interval_secs)
        if count >= int(sample_size / 2) :
            return True
        return False

    def update_cpu_stats(self) :
        size = int(self.sample_times / self.interval_secs)
        # cpu_stats stores the cpu usage in the passed sample_times * interval_secs
        if len(self.cpu_stats) == size + 1 :
            self.cpu_stats.pop(0)

        percent = psutil.cpu_percent(self.interval_secs)
        if percent > CPUMonitor.CPU_MEMORY_USAGE_THRESH :
            self._log()
        self.cpu_stats.append(percent)

    def run(self) :
        while True :
            self.update_cpu_stats()

class AlarmDaemon(threading.Thread) :
    def __init__(self, interval = 1) :
        threading.Thread.__init__(self)
        self.stop = threading.Event()
        self.interval = interval
        self.cpu_mon = CPUMonitor()
        self.cpu_mon.start()

    def run(self) :
        while not self.stop.wait(self.interval) :
            self.process()

    def process(self) :
        self.check_ntp_reachable()
        self.check_cpu_high()

    def check_ntp_reachable(self) :
        not_reach = Alarm("CHASSIS-1", "NTP_NOT_REACH", "MINOR", "false", "NTP SERVERS UNREACHABLE")
        ret = subprocess.getoutput("chronyc refresh")
        # chronyd is inactive
        if "506" in ret :
            not_reach.clear()
            return

        dbc = db.Client(db.HOST_DB, db.CONFIG_DB)
        ntp_servers = dbc.get_keys("NTP_SERVER")
        ntp_reach_result = 0
        for server in ntp_servers:
            cmd = f"sudo chronyc sources | grep {server} | awk "
            cmd += "'{print $1}'"
            #print(f"cmd ={cmd}")
            reach_info = subprocess.getoutput(cmd)
            #print(f"reach_info = {str(reach_info)}")
            if str(reach_info).strip() == "^*":
                ntp_reach_result |= 1
            else:
                ntp_reach_result |= 0

        #print(f"ntp_reach_result ={ntp_reach_result}")
        if ntp_reach_result == 0 and len(ntp_servers)>0:
            not_reach.create()
        else:
            not_reach.clear()

    def check_cpu_high(self) :
        cpu_hi = Alarm("CU-1", "CPU_USAGE_HIGH")
        if self.cpu_mon.cpu_high() :
            cpu_hi.create()
        else :
            cpu_hi.clear()


ad = AlarmDaemon()
ad.start()







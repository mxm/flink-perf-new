from lib import System

from cluster import hadoop, flink
from fabric.api import execute, local

class Hadoop(System):

    once_per_suite = True

    def __init__(self, config):
        self.config = config
        hadoop.conf = self.config

    def install(self):
        if 'install' not in self.skip_targets:
            execute(hadoop.install)

    def configure(self):
        if 'configure' not in self.skip_targets:
            execute(hadoop.configure)
        execute(hadoop.pull)

    def reset(self):
        #execute(hadoop.delete_data_slaves)
        pass

    def start(self):
        if 'start' not in self.skip_targets:
            execute(hadoop.master)
            execute(hadoop.slaves)

    def stop(self):
        execute(hadoop.slaves, 'stop')
        execute(hadoop.master, 'stop')

    def save_log(self, log_name):
        pass

    def __str__(self):
        return "hadoop"


class Flink(System):

    once_per_suite = False

    def __init__(self, config):
        self.config = config
        flink.conf = self.config

    def install(self):
        if 'install' not in self.skip_targets:
            execute(flink.install)

    def configure(self):
        if 'configure' not in self.skip_targets:
            execute(flink.configure)
        execute(flink.pull)

    def reset(self):
        pass

    def start(self):
        execute(flink.master)
        execute(flink.slaves)

    def stop(self):
        execute(flink.slaves, 'stop')
        execute(flink.master, 'stop')

    def save_log(self, unique_full_path):
        execute(flink.copy_log_master, unique_full_path)
        execute(flink.copy_log_slaves, unique_full_path)

    def __str__(self):
        return "flink"

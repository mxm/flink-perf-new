from lib import System

from cluster import hadoop, flink
from fabric.api import execute

class Hadoop(System):

    def __init__(self, config):
        self.config = config
        hadoop.conf = self.config

    def install(self):
        execute(hadoop.install)

    def configure(self):
        execute(hadoop.configure)
        execute(hadoop.pull)

    def reset(self):
        execute(hadoop.delete_data_slaves)

    def start(self):
        execute(hadoop.master)
        execute(hadoop.slaves)

    def stop(self):
        execute(hadoop.slaves, 'stop')
        execute(hadoop.master, 'stop')


class Flink(System):

    def __init__(self, config):
        self.config = config
        flink.conf = self.config

    def install(self):
        execute(flink.install)

    def configure(self):
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
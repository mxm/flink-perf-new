from core.lib import Benchmark, Generator, ClusterSuite

# import cluster and systems classes
from core.clusters import ComputeEngine
from core.systems import Hadoop, Flink

# import standard configs
from configs import compute_engine_config, hadoop_config, flink_config

# import experiment's main class
from experiments.wordcount_new import WordCountNew
from experiments.grep import Grep

# import data generators for benchmarks
from experiments import generators

# Aljoscha's project
compute_engine_config['project_name'] = "astral-sorter-757"
# machine prefix
compute_engine_config['prefix'] = "nightly-benchmark-"
# 2 cores 7.5GB RAM
compute_engine_config['machine_type'] = "n1-standard-2"
# num cores to use
compute_engine_config['num_cores'] = 2
compute_engine_config['size_mem'] = 7500
# 16 workers + 1 master
compute_engine_config['num_workers'] = 10
compute_engine_config['disk_space_gb'] = 200

dop = compute_engine_config['num_workers'] * compute_engine_config['num_cores']

flink_config['num_task_slots'] = compute_engine_config['num_cores']
flink_config['taskmanager_heap'] = 5120 #5gb
flink_config['jobmanager_heap'] = 5120
flink_config['parallelization'] = dop

cluster = ComputeEngine(compute_engine_config)
hadoop = Hadoop(hadoop_config)
flink = Flink(flink_config)

systems = [hadoop, flink]

benchmarks = [

    Benchmark(
        id = "WordCount",
        systems = [flink],
        experiment = WordCountNew(),
        times = 3
    ),

    Benchmark(
        id = "Grep",
        systems = [flink],
        experiment = Grep(),
        times = 3
    ),

    # KMeans
    # PageRank
    # ALS

]


generators = [
    Generator(
        id = "TextGenerator",
        systems = [flink],
        experiment = generators.Text(
            size_gb = 150, # 5gb * 10 nodes * 3
            dop = dop
        )
    )
]

suite = ClusterSuite("NightlySuite", cluster, systems, generators, benchmarks)

suite.execute(retry_setup=0,
              shutdown_on_failure=True,
              email_results=True)

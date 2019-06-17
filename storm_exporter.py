#!/usr/bin/python3
import time
import sys
import requests
import telnetlib
from prometheus_client import start_http_server, Gauge, Info

# CLUSTER/SUMMARY METEICS
STORM_CLUSTER_UP = Gauge('storm_up', 'Storm up')
STORM_CLUSTER_TIME_SECOND = Gauge(
    'storm_up_time_seconds', 'Shows since how long the nimbus has been running in seconds')
STORM_CLUSTER_SUPERVIORS = Gauge(
    'storm_cluster_supervisors', 'Number of supervisors running')
STORM_CLUSTER_TOPOLOGIES = Gauge(
    'storm_cluster_topologies', 'Number of topologies running')
STORM_CLUSTER_SLOTS_TOTAL = Gauge(
    'storm_cluster_slots_total', 'Total number of available worker slots')
STORM_CLUSTER_SLOTS_USED = Gauge(
    'storm_cluster_slots_used', 'Number of worker slots used')
STORM_CLUSTER_SLOTS_FREE = Gauge(
    'storm_cluster_slots_free', 'Number of worker slots available')
STORM_CLUSTER_EXECUTORS_TOTAL = Gauge(
    'storm_cluster_executors_total', 'Total number of executors')
STORM_CLUSTER_TASKS_TOTAL = Gauge('storm_cluster_tasks_total', 'Total tasks')
STORM_CLUSTER_SCHEDULER_DISPLAY_RESOURCE = Gauge(
    'storm_cluster_scheduler_display_resource', 'Whether to display scheduler resource information')
STORM_CLUSTER_TOTAL_MEM = Gauge(
    'storm_cluster_total_mem', 'The total amount of memory in the cluster in MB')
STORM_CLUSTER_TOTAL_CPU = Gauge(
    'storm_cluster_total_cpu', 'The total amount of CPU in the cluster')
STORM_CLUSTER_AVAIL_CPU = Gauge(
    'storm_cluster_avail_cpu', 'The amount of available cpu in the cluster')
STORM_CLUSTER_AVAIL_MEM = Gauge(
    'storm_cluster_avail_mem', 'The amount of available memory in the cluster in MB')
STORM_CLUSTER_MEM_ASSIGNED_PERCENTUTIL = Gauge(
    'storm_cluster_mem_assigned_aercentutil', 'The percent utilization of assigned memory resources in cluster')
STORM_CLUSTER_CPU_ASSIGNED_PERCENTUTIL = Gauge(
    'storm_cluster_cpu_assigned_aercentutil', 'The percent utilization of assigned cpu resources in cluster')


# SUPERVISOR/SUMMARY METRICS
STORM_SUPERVISOR_UPTIME_SECONDS = Gauge(
    'storm_supervisor_uptime_seconds', 'Shows how long the supervisor is running in seconds', ['SupervisorName'])
STORM_SUPERVISOR_SLOTS_TOTAL = Gauge(
    'storm_supervisor_slots_total', 'Total number of available worker slots for this supervisor', ['SupervisorName'])
STORM_SUPERVISOR_SLOTS_USED = Gauge(
    'storm_supervisor_slots_used', 'Number of worker slots used on this supervisor', ['SupervisorName'])
STORM_SUPERVISOR_SLOTS_FREE = Gauge(
    'storm_supervisor_slots_free', 'Number of worker slots available', ['SupervisorName'])
STORM_SUPERVISOR_TOTAL_MEM = Gauge(
    'storm_supervisor_total_mem', 'Total memory capacity on this supervisor', ['SupervisorName'])
STORM_SUPERVISOR_TOTAL_CPU = Gauge(
    'storm_supervisor_total_cpu', 'Total CPU capacity on this supervisor', ['SupervisorName'])
STORM_SUPERVISOR_AVAIL_CPU = Gauge(
    'storm_supervisor_avail_cpu', 'The amount of available cpu in the supervisor', ['SupervisorName'])
STORM_SUPERVISOR_AVAIL_MEM = Gauge(
    'storm_supervisor_avail_mem', 'The amount of available memory in the supervisor in MB', ['SupervisorName'])
STORM_SUPERVISOR_USED_MEM = Gauge(
    'storm_supervisor_used_mem', 'Used memory capacity on this supervisor', ['SupervisorName'])
STORM_SUPERVISOR_USED_CPU = Gauge(
    'storm_supervisor_used_cpu', 'Used CPU capacity on this supervisor', ['SupervisorName'])

# TOPOLOGY/SUMMARY METRICS
STORM_TOPOLOGY_STATUS = Info(
    'storm_topology_status', 'Shows topology status', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_UPTIME_SECONDS = Gauge(
    'storm_topology_uptime_seconds', 'Shows how long the topology is running in seconds', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_TASKS_TOTAL = Gauge(
    'storm_topology_tasks_total', 'Total number of tasks for this topology', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_WORKERS_TOTAL = Gauge(
    'storm_topology_workers_total', 'Number of workers used for this topology', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_EXECUTORS_TOTAL = Gauge(
    'storm_topology_executors_total', 'Number of executors used for this topology', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_REPLICATION_COUNT = Gauge(
    'storm_topology_replication_count', 'Number of nimbus hosts on which this topology code is replicated', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_REQUESTED_MEM_ON_HEAP = Gauge(
    'storm_topology_requested_mem_on_heap', 'Requested On-Heap Memory by User (MB)', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_REQUESTED_MEM_OFF_HEAP = Gauge(
    'storm_topology_requested_mem_off_heap', 'Requested Off-Heap Memory by User (MB)', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_REQUESTED_TOTAL_MEM = Gauge(
    'storm_topology_requested_total_mem', 'Requested Total Memory by User (MB)', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_REQUESTED_CPU = Gauge(
    'storm_topology_requested_cpu', 'Requested CPU by User (%)', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_ASSIGNED_MEM_ON_HEAP = Gauge(
    'storm_topology_assigned_mem_on_heap', 'Assigned On-Heap Memory by Scheduler (MB)', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_ASSIGNED_MEM_OFF_HEAP = Gauge(
    'storm_topology_assigned_mem_off_heap', 'Assigned Off-Heap Memory by Scheduler (MB)', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_ASSIGNED_TOTAL_MEM = Gauge(
    'storm_topology_assigned_total_mem', 'Assigned Total Memory by Scheduler (MB)', ['TopologyName', 'TopologyId'])
STORM_TOPOLOGY_ASSIGNED_CPU = Gauge(
    'storm_topology_assigned_cpu', 'Assigned CPU by Scheduler (%)', ['TopologyName', 'TopologyId'])

# TOPOLOGY/STATS METRICS:
TOPOLOGY_STATS_TRASFERRED = Gauge('storm_topology_stats_trasferred', 'Number messages transferred in given window', [
                                  'TopologyName', 'TopologyId', 'window'])
TOPOLOGY_STATS_EMITTED = Gauge('storm_topology_stats_emitted', 'Number of messages emitted in given window', [
                               'TopologyName', 'TopologyId', 'window'])
TOPOLOGY_STATS_COMPLETE_LATENCY = Gauge('storm_topology_stats_complete_latency', 'Total latency for processing the message', [
                                        'TopologyName', 'TopologyId', 'window'])
TOPOLOGY_STATS_ACKED = Gauge('storm_topology_stats_acked', 'Number of messages acked in given window', [
                             'TopologyName', 'TopologyId', 'window'])
TOPOLOGY_STATS_FAILED = Gauge('storm_topology_stats_failed', 'Number of messages failed in given window', [
                              'TopologyName', 'TopologyId', 'window'])

# TOPOLOGY/ID SPOUT METRICS:
STORM_TOPOLOGY_SPOUTS_EXECUTORS = Gauge('storm_topology_spouts_executors', 'Number of executors for the spout', [
                                        'TopologyName', 'TopologyId', 'SpoutId'])
STORM_TOPOLOGY_SPOUTS_EMITTED = Gauge('storm_topology_spouts_emitted', 'Number of messages emitted in given window', [
                                      'TopologyName', 'TopologyId', 'SpoutId'])
STORM_TOPOLOGY_SPOUTS_COMPLETE_LATENCY = Gauge(
    'storm_topology_spouts_complete_latency', 'Total latency for processing the message', ['TopologyName', 'TopologyId', 'SpoutId'])
STORM_TOPOLOGY_SPOUTS_TRANSFERRED = Gauge('storm_topology_spouts_transferred', 'Total number of messages transferred in given window', [
                                          'TopologyName', 'TopologyId', 'SpoutId'])
STORM_TOPOLOGY_SPOUTS_TASKS = Gauge('storm_topology_spouts_tasks', 'Total number of tasks for the spout', [
                                    'TopologyName', 'TopologyId', 'SpoutId'])
STORM_TOPOLOGY_SPOUTS_ACKED = Gauge('storm_topology_spouts_acked', 'Number of messages acked', [
                                    'TopologyName', 'TopologyId', 'SpoutId'])
STORM_TOPOLOGY_SPOUTS_FAILED = Gauge('storm_topology_spouts_failed', 'Number of messages failed', [
                                     'TopologyName', 'TopologyId', 'SpoutId'])

# TOPOLOGY/ID BOLT METRICS:
STORM_TOPOLOGY_BOLTS_PROCESS_LATENCY = Gauge(
    'storm_topology_bolts_process_latency', 'Average time of the bolt to ack a message after it was received', ['TopologyName', 'TopologyId', 'BoltId'])
STORM_TOPOLOGY_BOLTS_CAPACITY = Gauge(
    'storm_topology_bolts_capacity', 'This value indicates number of messages executed * average execute latency / time window', ['TopologyName', 'TopologyId', 'BoltId'])
STORM_TOPOLOGY_BOLTS_EXECUTE_LATENCY = Gauge(
    'storm_topology_bolts_execute_latency', 'Average time to run the execute method of the bolt', ['TopologyName', 'TopologyId', 'BoltId'])
STORM_TOPOLOGY_BOLTS_EXECUTORS = Gauge('storm_topology_bolts_executors', 'Number of executor tasks in the bolt component', [
                                       'TopologyName', 'TopologyId', 'BoltId'])
STORM_TOPOLOGY_BOLTS_TASKS = Gauge('storm_topology_bolts_tasks', 'Number of instances of bolt', [
                                   'TopologyName', 'TopologyId', 'BoltId'])
STORM_TOPOLOGY_BOLTS_ACKED = Gauge('storm_topology_bolts_acked', 'Number of tuples acked by the bolt', [
                                   'TopologyName', 'TopologyId', 'BoltId'])
STORM_TOPOLOGY_BOLTS_FAILED = Gauge('storm_topology_bolts_failed', 'Number of tuples failed by the bolt', [
                                    'TopologyName', 'TopologyId', 'BoltId'])
STORM_TOPOLOGY_BOLTS_EMITTED = Gauge('storm_topology_bolts_emitted', 'of tuples emitted by the bolt', [
                                     'TopologyName', 'TopologyId', 'BoltId'])


def getMetric(metric):
    if metric == None:
        return 0
    else:
        return metric


def statsMetric(stat, tn, tid):
    wd = stat['window']
    TOPOLOGY_STATS_TRASFERRED.labels(tn, tid, wd).set(
        getMetric(stat['transferred']))
    TOPOLOGY_STATS_EMITTED.labels(tn, tid, wd).set(getMetric(stat['emitted']))
    TOPOLOGY_STATS_COMPLETE_LATENCY.labels(
        tn, tid, wd).set(getMetric(stat['completeLatency']))
    TOPOLOGY_STATS_ACKED.labels(tn, tid, wd).set(getMetric(stat['acked']))
    TOPOLOGY_STATS_FAILED.labels(tn, tid, wd).set(getMetric(stat['failed']))


def spoutMetric(spout, tn, tid):
    sid = spout['spoutId']
    STORM_TOPOLOGY_SPOUTS_EXECUTORS.labels(
        tn, tid, sid).set(getMetric(spout['executors']))
    STORM_TOPOLOGY_SPOUTS_EMITTED.labels(
        tn, tid, sid).set(getMetric(spout['emitted']))
    STORM_TOPOLOGY_SPOUTS_COMPLETE_LATENCY.labels(
        tn, tid, sid).set(getMetric(spout['completeLatency']))
    STORM_TOPOLOGY_SPOUTS_TRANSFERRED.labels(
        tn, tid, sid).set(getMetric(spout['transferred']))
    STORM_TOPOLOGY_SPOUTS_TASKS.labels(
        tn, tid, sid).set(getMetric(spout['tasks']))
    STORM_TOPOLOGY_SPOUTS_ACKED.labels(
        tn, tid, sid).set(getMetric(spout['acked']))
    STORM_TOPOLOGY_SPOUTS_FAILED.labels(
        tn, tid, sid).set(getMetric(spout['failed']))


def boltMetric(bolt, tn, tid):
    bid = bolt['boltId']
    STORM_TOPOLOGY_BOLTS_CAPACITY.labels(tn, tid, bid).set(
        getMetric(bolt['processLatency']))
    STORM_TOPOLOGY_BOLTS_PROCESS_LATENCY.labels(
        tn, tid, bid).set(getMetric(bolt['capacity']))
    STORM_TOPOLOGY_BOLTS_EXECUTE_LATENCY.labels(
        tn, tid, bid).set(getMetric(bolt['executeLatency']))
    STORM_TOPOLOGY_BOLTS_EXECUTORS.labels(
        tn, tid, bid).set(getMetric(bolt['executors']))
    STORM_TOPOLOGY_BOLTS_TASKS.labels(
        tn, tid, bid).set(getMetric(bolt['tasks']))
    STORM_TOPOLOGY_BOLTS_ACKED.labels(
        tn, tid, bid).set(getMetric(bolt['acked']))
    STORM_TOPOLOGY_BOLTS_FAILED.labels(
        tn, tid, bid).set(getMetric(bolt['failed']))
    STORM_TOPOLOGY_BOLTS_EMITTED.labels(
        tn, tid, bid).set(getMetric(bolt['emitted']))


def topologyMetric(topology):
    tn = topology['name']
    tid = topology['id']
    for stat in topology['topologyStats']:
        statsMetric(stat, tn, tid)
    for spout in topology['spouts']:
        spoutMetric(spout, tn, tid)
    for bolt in topology['bolts']:
        boltMetric(bolt, tn, tid)


def topologySummaryMetric(topology_summary, stormUiHost):
    tn = topology_summary['name']
    tid = topology_summary['id']
    STORM_TOPOLOGY_STATUS.labels(tn, tid).info(
        {'status': topology_summary['status']})
    STORM_TOPOLOGY_UPTIME_SECONDS.labels(tn, tid).set(
        topology_summary['uptimeSeconds'])
    STORM_TOPOLOGY_TASKS_TOTAL.labels(tn, tid).set(
        topology_summary['tasksTotal'])
    STORM_TOPOLOGY_WORKERS_TOTAL.labels(tn, tid).set(
        topology_summary['workersTotal'])
    STORM_TOPOLOGY_EXECUTORS_TOTAL.labels(tn, tid).set(
        topology_summary['executorsTotal'])
    STORM_TOPOLOGY_REPLICATION_COUNT.labels(tn, tid).set(
        topology_summary['replicationCount'])
    STORM_TOPOLOGY_REQUESTED_MEM_ON_HEAP.labels(
        tn, tid).set(topology_summary['requestedMemOnHeap'])
    STORM_TOPOLOGY_REQUESTED_MEM_OFF_HEAP.labels(
        tn, tid).set(topology_summary['requestedMemOffHeap'])
    STORM_TOPOLOGY_REQUESTED_TOTAL_MEM.labels(
        tn, tid).set(topology_summary['requestedTotalMem'])
    STORM_TOPOLOGY_REQUESTED_CPU.labels(tn, tid).set(
        topology_summary['requestedCpu'])
    STORM_TOPOLOGY_ASSIGNED_MEM_ON_HEAP.labels(
        tn, tid).set(topology_summary['assignedMemOnHeap'])
    STORM_TOPOLOGY_ASSIGNED_MEM_OFF_HEAP.labels(
        tn, tid).set(topology_summary['assignedMemOffHeap'])
    STORM_TOPOLOGY_ASSIGNED_TOTAL_MEM.labels(
        tn, tid).set(topology_summary['assignedTotalMem'])
    STORM_TOPOLOGY_ASSIGNED_CPU.labels(tn, tid).set(
        topology_summary['assignedCpu'])

    try:
        r = requests.get('http://' + stormUiHost + '/api/v1/topology/' + tid)
        topologyMetric(r.json())
    except requests.exceptions.RequestException as e:
        print(e)


def clusterSummaryMetric(clusterStorm):
    STORM_CLUSTER_UP.set(1)
    STORM_CLUSTER_SUPERVIORS.set(clusterStorm['supervisors'])
    STORM_CLUSTER_TOPOLOGIES.set(clusterStorm['topologies'])
    STORM_CLUSTER_SLOTS_TOTAL.set(clusterStorm['slotsTotal'])
    STORM_CLUSTER_SLOTS_USED.set(clusterStorm['slotsUsed'])
    STORM_CLUSTER_SLOTS_FREE.set(clusterStorm['slotsFree'])
    STORM_CLUSTER_EXECUTORS_TOTAL.set(clusterStorm['executorsTotal'])
    STORM_CLUSTER_TASKS_TOTAL.set(clusterStorm['tasksTotal'])
    STORM_CLUSTER_SCHEDULER_DISPLAY_RESOURCE.set(
        clusterStorm['schedulerDisplayResource'])
    STORM_CLUSTER_TOTAL_MEM.set(clusterStorm['totalMem'])
    STORM_CLUSTER_TOTAL_CPU.set(clusterStorm['totalCpu'])
    STORM_CLUSTER_AVAIL_CPU.set(clusterStorm['availCpu'])
    STORM_CLUSTER_AVAIL_MEM.set(clusterStorm['availMem'])
    STORM_CLUSTER_MEM_ASSIGNED_PERCENTUTIL.set(
        clusterStorm['memAssignedPercentUtil'])
    STORM_CLUSTER_CPU_ASSIGNED_PERCENTUTIL.set(
        clusterStorm['cpuAssignedPercentUtil'])


def nimbusSummaryMetric(nimbusStorm):
    STORM_CLUSTER_TIME_SECOND.set(nimbusStorm['nimbusUpTimeSeconds'])


def supervisorSummaryMetric(supervisor):
    SupervisorName = supervisor['host']
    STORM_SUPERVISOR_UPTIME_SECONDS.labels(
        SupervisorName).set(supervisor['uptimeSeconds'])
    STORM_SUPERVISOR_SLOTS_TOTAL.labels(
        SupervisorName).set(supervisor['slotsTotal'])
    STORM_SUPERVISOR_SLOTS_USED.labels(
        SupervisorName).set(supervisor['slotsUsed'])
    STORM_SUPERVISOR_SLOTS_FREE.labels(
        SupervisorName).set(supervisor['slotsFree'])
    STORM_SUPERVISOR_TOTAL_MEM.labels(
        SupervisorName).set(supervisor['totalMem'])
    STORM_SUPERVISOR_TOTAL_CPU.labels(
        SupervisorName).set(supervisor['totalCpu'])
    STORM_SUPERVISOR_AVAIL_CPU.labels(
        SupervisorName).set(supervisor['availCpu'])
    STORM_SUPERVISOR_AVAIL_MEM.labels(
        SupervisorName).set(supervisor['availMem'])
    STORM_SUPERVISOR_USED_MEM.labels(SupervisorName).set(supervisor['usedMem'])
    STORM_SUPERVISOR_USED_CPU.labels(SupervisorName).set(supervisor['usedCpu'])


if(len(sys.argv) != 5):
    print(
        'Missing arguments, Usage storm-metrics-consumer.py [StormUI Host] [HTTP port of the consumer] [Refresh Rate in Seconds] [Max Retries]')
    sys.exit(-1)

stormUiHost = str(sys.argv[1])
stormUiHostPort = stormUiHost.split(":")
if len(stormUiHostPort) != 2:
    print("Invalid stormUiHost")
    print("Exit -2")
    sys.exit(-2)
stormHost = stormUiHostPort[0]
stormPort = stormUiHostPort[1]
httpPort = int(sys.argv[2])
refreshRate = int(sys.argv[3])
i = 1
maxRetries = int(sys.argv[4])

start_http_server(httpPort)

while True:
    try:
        telnetlib.Telnet(stormHost, stormPort)
    except Exception as e:
        print(e)
    else:
        try:
            clusterStorm = requests.get(
                'http://' + stormUiHost + '/api/v1/cluster/summary')
            print('cluster metrics')
            clusterSummaryMetric(clusterStorm.json())

            nimbusStorm = requests.get(
                'http://' + stormUiHost + '/api/v1/nimbus/summary')
            print('nimbus metrics')
            for nimbus in nimbusStorm.json()['nimbuses']:
                nimbusSummaryMetric(nimbus)

            supervisorStrom = requests.get(
                'http://' + stormUiHost + '/api/v1/supervisor/summary')
            print('supervison metrics')
            for supervisor in supervisorStrom.json()['supervisors']:
                supervisorSummaryMetric(supervisor)

            topologyStorm = requests.get(
                'http://' + stormUiHost + '/api/v1/topology/summary')
            print('caught metrics')
            for topology in topologyStorm.json()['topologies']:
                topologySummaryMetric(topology, stormUiHost)

        except requests.exceptions.RequestException as e:
            print(e)
            if i >= maxRetries:
                print("Retry times: %d" % i)
                print("Exit 1")
                sys.exit(1)
            else:
                print("Retry times: %d" % i)
                i += 1
    time.sleep(refreshRate)

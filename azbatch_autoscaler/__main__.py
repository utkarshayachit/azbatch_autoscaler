import argparse
import time
import logging

parser = argparse.ArgumentParser('azbatch_autoscaler', description='Scale Azure Batch pools')
parser.add_argument('--endpoint', dest='endpoint', required=True, help='The Azure Batch endpoint')
parser.add_argument('--pool-id', dest='pool_id', required=True, help='The ID of the pool to scale')
parser.add_argument('--min-nodes', dest='min_nodes', type=int, default=0, help='The minimum number of dedicated nodes to scale to (default: 0)')
parser.add_argument('--max-nodes', dest='max_nodes', type=int, required=True, help='The maximum number of dedicated nodes to scale to ')
parser.add_argument('--low-priority-nodes', dest='low_priority_nodes', type=int, required=True, help='The number of low priority nodes to scale to')
parser.add_argument('--interval', dest='interval', type=int, default=0, help='The interval in between two checks in seconds. If 0, the script will run once and exit. (default: 0)')
parser.add_argument('--log-level', dest='log_level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    help='The log level (default: INFO)')

args = parser.parse_args()

from . import logger
logger.set_default_log_level(args.log_level)
log = logger.get_logger(__name__)
log.info('Scaling pool "%s" to at least %d and at most %d dedicated nodes and %d low priority nodes', args.pool_id, args.min_nodes, args.max_nodes, args.low_priority_nodes)

from . import utils

while True:
    utils.scale_pool(args.endpoint, args.pool_id, args.min_nodes, args.max_nodes, args.low_priority_nodes)
    if args.interval <= 0:
        log.info('Exiting')
        break
    time.sleep(args.interval)

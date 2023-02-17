# Batch Pool Scaling Utility

Azure Batch provides the ability to rescale pools automatically. However, currently the pool autoscaling script cannot
determine how many spot instances in the pool have been preempted. Thus, a use-case where one wants to update the target
dedicated node count of a pool based on number of spot nodes preempted is not possible. This utility provides a solution.

It can be run once to update the pool size. It can also run as a daemon to continuously monitor the pool and update the
pool size based on the number of spot nodes preempted.

## Installation

The project and its dependencies can be installed using pip.

```bash
git checkout https://github.com/utkarshayachit/azbatch_autoscaler
cd azbatch_autoscaler
pip install .
```

## Usage

```bash
azbatch_autoscaler [-h] --endpoint ENDPOINT --pool-id POOL_ID [--min-nodes MIN_NODES] --max-nodes MAX_NODES --low-priority-nodes LOW_PRIORITY_NODES [--interval INTERVAL] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Scale Azure Batch pools

options:
  -h, --help            show this help message and exit
  --endpoint ENDPOINT   The Azure Batch endpoint
  --pool-id POOL_ID     The ID of the pool to scale
  --min-nodes MIN_NODES
                        The minimum number of dedicated nodes to scale to (default: 0)
  --max-nodes MAX_NODES
                        The maximum number of dedicated nodes to scale to
  --low-priority-nodes LOW_PRIORITY_NODES
                        The number of low priority nodes to scale to
  --interval INTERVAL   The interval in between two checks in seconds. If 0, the script will run once and exit. (default: 0)
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
```

## Examples

For example, to rescale a pool where it can have 10 nodes, with at least 1 dedicated node, and the rest
can be spot instances, if possible, we can run the following command.

```bash
python -m azbatch_autoscaler                              \
    --endpoint <batch-account>.<region>.batch.azure.com   \
    --pool-id <pool-id>                                   \
    --min-nodes 1 --max-nodes 10                          \
    --low-priority-nodes 9
```

This will update the pool size, if needed, each time the script is run. To have the script run continuously,
check the pool size every 5 minutes, we can run the following command.

```bash
python -m azbatch_autoscaler                              \
    --endpoint <batch-account>.<region>.batch.azure.com   \
    --pool-id <pool-id>                                   \
    --min-nodes 1 --max-nodes 10                          \
    --low-priority-nodes 9                                \
    --interval 300
```

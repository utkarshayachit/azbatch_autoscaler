from azure.batch import BatchServiceClient, models
from azure.identity import DefaultAzureCredential

from . import azure_identity_credential_adapter

from . import logger
log = logger.get_logger(__name__)

def login(endpoint):
    credentials = DefaultAzureCredential()
    wrapper = azure_identity_credential_adapter.AzureIdentityCredentialAdapter(credentials, resource_id='https://batch.core.windows.net/')
    batch_client = BatchServiceClient(wrapper, batch_url="https://{}".format(endpoint))
    return batch_client

def pool_resize(endpoint, pool_id, targetDedicatedNodes, targetLowPriorityNodes):
    """Resize a pool"""
    log.info('Resizing pool "%s" to %d dedicated nodes and %d low priority nodes', pool_id, targetDedicatedNodes, targetLowPriorityNodes)
    client = login(endpoint)
    client.pool.resize(pool_id,
        models.PoolResizeParameter(target_dedicated_nodes=targetDedicatedNodes,
                target_low_priority_nodes=targetLowPriorityNodes))
    
def get_preempted_nodes_count(endpoint, pool_id):
    """Get a list of preempted nodes"""
    client = login(endpoint)
    nodes = client.compute_node.list(pool_id)
    preempted_nodes = filter(lambda x: x.state == models.ComputeNodeState.preempted, nodes)
    return len(list(preempted_nodes))

def scale_pool(endpoint, pool_id, min_nodes, max_nodes, max_low_priority_nodes):
    """Auto scale a pool"""
    preempted_nodes = get_preempted_nodes_count(endpoint, pool_id)
    log.info('Found %d preempted nodes', preempted_nodes)

    target_nodes = min(min_nodes + preempted_nodes, max_nodes)
    log.info('Will need %d dedicated nodes', target_nodes)
    pool_resize(endpoint, pool_id, target_nodes, max_low_priority_nodes)

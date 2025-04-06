from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
# Load environment variables (optional)

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "127.0.0.1")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "traffic_zen")
# CASSANDRA_USERNAME = os.getenv("CASSANDRA_USERNAME", "cassandra")
# CASSANDRA_PASSWORD = os.getenv("CASSANDRA_PASSWORD", "cassandra")

cluster = None
session = None

def get_cassandra_session():
    """Returns a Cassandra session using dependency injection."""
    return session

def startup():

    """Initialize Cassandra session at application startup."""
    global cluster, session
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect()
    session.set_keyspace(CASSANDRA_KEYSPACE)
    print("Cassandra session initialized...")
    
def shutdown():
    global cluster
    if cluster:
        cluster.shutdown()
        print("Cassandra session closed.")



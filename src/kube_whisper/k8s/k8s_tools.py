"""
Kubernetes tools and utilities.
"""

from kubernetes import client, config


class K8sTools:
    def __init__(self):
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

    def list_pods(self, namespace="default"):
        """List all pods in the specified namespace"""
        return self.v1.list_namespaced_pod(namespace)

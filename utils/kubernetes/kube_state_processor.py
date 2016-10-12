

class KubeStateProcessor:
    def __init__(self, kubernetes_check):
        self.kube_check = kubernetes_check

    def process(self, message):
        try:
            getattr(self, message.name)(message)
        except AttributeError:
            self.kube_check.log.debug("Unable to handle metric: {}".format(message.name))

    def kube_node_status_capacity_cpu_cores(self, message):
        metric_name = 'kubernetes.node.cpu_capacity'
        for metric in message.metric:
            val = metric.gauge.value
            tags = ['host:{}'.format(metric.label[0].value)]
            self.kube_check.publish_gauge(self, metric_name, val, tags)

def test_service(host):
    service = host.service('couchbase-server')
    assert service.is_running
    assert service.is_enabled


def test_port(host):
    socket = host.socket("tcp://0.0.0.0:8091")
    assert socket.is_listening

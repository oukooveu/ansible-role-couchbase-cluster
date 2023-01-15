def test_service(host):
    service = host.service('couchbase-server')
    assert service.is_running
    assert service.is_enabled


def test_port(host):
    socket = host.socket("tcp://0.0.0.0:8091")
    assert socket.is_listening


def test_n1ql(host):
    cmd = host.run("/opt/couchbase/bin/cbq -u alice -p mysecret -q -s 'SELECT a.name FROM `travel-sample`.inventory.airline a WHERE a.callsign = \"SPEEDBIRD\";'")
    assert cmd.succeeded
    result = eval(cmd.stdout)
    assert result['results'][0]['name'] == "British Airways"

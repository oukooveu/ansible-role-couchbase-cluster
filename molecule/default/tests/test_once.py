testinfra_hosts = ["node1.local"]

def test_n1ql(host):
    cmd = host.run("/opt/couchbase/bin/cbq -u alice -p mysecret -q -s 'SELECT a.name FROM `travel-sample`.inventory.airline a WHERE a.callsign = \"SPEEDBIRD\";'")
    result = json.loads(cmd.stdout)
    assert result.get('status', 'failed') == 'success'
    assert result['results'][0]['name'] == "British Airways"

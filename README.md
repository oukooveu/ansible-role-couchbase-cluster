# Couchbase cluster ansible role
[![Molecule](https://github.com/oukooveu/ansible-role-couchbase-cluster/actions/workflows/molecule.yml/badge.svg)](https://github.com/oukooveu/ansible-role-couchbase-cluster/actions/workflows/molecule.yml)

This role is created to provide a simple way to bootstrap and configure (through REST API) Couchbase cluster. There is [ansible role](https://github.com/couchbaselabs/ansible-couchbase-server) provided by vendor, but it was updated two years ago, most probably outdated and configures cluster through CLI commands while proper way to do this is to write dedicated ansible module (this was not done by myself because for my needs it's enough just to bootstrap cluster and configure buckets and users).

The role provides following:
- install couchbase server on all nodes;
- initialize couchbase cluster;
- join all nodes to the cluster;
- add configured buckets;
- add configured users.

Important considerations:
- role works only for couchbase server version greater then 7.1.x (`clusterInit` REST API method only available from 7.1 is used);
- bucket and users are only created and not deleted;
- buckets should exist if RBAC based on buckets (like `bucket_full_access[travel-sample]`) is used.

## Requirements

There are no special requirements, everything is installed through Couchbase package.

## Role Variables

| Variable | Description | Default value |
|----------|-------------|---------------|
| couchbase_release_version | Version of couchbase meta package (configures package manager) | `1.0` |
| couchbase_server_version | Couchbase server version. To list all available packages use `apt list -a couchbase-server` for Debian or `yum list --showduplicates couchbase-server` for RHEL | `7.1.3-3479` |
| couchbase_cluster_name | Couchbase cluster name | `cbc-dc1` |
| couchbase_host_address | The host address for couchbase nodes. If default value is not suitable (for example addresses from dedicated private network is in use) provide addresses for all nodes through host variables | `{{ ansible_default_ipv4.address }}` |
| couchbase_admin_user | Couchbase admin user, can only be setup on cluster initialization | `admin` |
| couchbase_admin_password | Couchbase admin password, can only be setup on cluster initialization | `password` |
| couchbase_services | Comma separated list fo services are assigned to node in the cluster. For different service on different nodes put it into host vars | `kv,n1ql,index` |
| couchbase_data_memory_quota | Couchbase data (kv) service memory quota in megabytes | `512` |
| couchbase_index_memory_quota | Couchbase index service memory quota in megabytes | `1024` |
| couchbase_index_storage_mode | Couchbase index storage mode | `plasma` |
| couchbase_bucket_defaults | Default options for buckets | see defaults/main.yml for details |
| couchbase_buckets | List of buckets to be created | `[]`, mandatory option: `name` |
| couchbase_user_defaults | Default options for users | see defaults/main.yml for details |
| couchbase_users | List of users to be created | `[]`, mandatory options: `name` (user name) and `password` (user password) |

## Example Playbook

```
- name: install couchbase cluster
  hosts: all
  vars:
    couchbase_server_version: '7.1.3-3479'
    couchbase_buckets:
      - name: 'just-a-bucket'
        replicaNumber: 0
        ramQuota: 100
    couchbase_users:
      - name: 'alice'
        password: 'mysecret'
        roles: 'bucket_full_access[just-a-bucket]'
      - name: 'bob'
        password: 'hissecret'
  roles:
    - role: oukooveu.couchbase_cluster
```

## Molecule tests

To run tests locally:
```
python -m venv .venv
. .venv/bin/activate
pip install -r molecule/default/requirements.txt
molecule test
```

To run tests for non-default image (`debian:10`) set `MOLECULE_IMAGE` environment variable to an appropriate value, for example:
```
export MOLECULE_IMAGE=rockylinux:8
```

If you just want to run Couchbase server this can be done by changing last command to `molecule converge`.

To cleanup test environment run `molecule destroy`.

## License

Apache 2.0

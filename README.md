# VastControl

## Description

VastControl is a Python CLI that lets you easily manage your instances on the Vast.ai platform.
This tool lets you list, rename and delete instances, and add SSH keys to an instance via its label.

# Requirements

- [Python 3](https://www.python.org/download/releases/3.0/)

- Vast.ai pip package : `pip install --upgrade vastai;` (then type `vastai set api-key YOUR_API_KEY`)

- Change the api key on line 47 of vastcontrol.py

# Usage

VastControl can be run from the CLI and rapidly embedded within existing python applications.

```bash
usage: vastcontrol.py [-h] [--list-up] [--rename RENAME] [--to TO] [--delete DELETE] [--label LABEL] [--add-ssh]

Managing Vast.ai instances

options:
  -h, --help       show this help message and exit
  --list-up        List running instances and their specifications
  --rename RENAME  ID of instance to be renamed
  --to TO          New name for the instance
  --delete DELETE  Delete an instance by its label
  --label LABEL    Instance label for adding an SSH key
  --add-ssh        Adding an SSH key to an instance
```


## Examples

List running instances and their specifications : 

```bash
└─$ python3 vastcontrol.py --list-up
ID: 12741302, Label: None, Status: loading
GPU: 1x RTX 2070S, vCPUs: 32, RAM: 503.8 GB, Storage: 72.5 GB
Price: $0.003/hr, Image: dizcza/docker-hashcat:cuda
Net Up: 1722.7 Mbps, Net Down: 1124.7 Mbps
------------------------------------------------------------
ID: 12741303, Label: None, Status: running
GPU: 1x RTX 2070, vCPUs: 24, RAM: 19.4 GB, Storage: 72.5 GB
Price: $0.113/hr, Image: dizcza/docker-hashcat:cuda
Net Up: 370.8 Mbps, Net Down: 384.9 Mbps
------------------------------------------------------------
ID: 12741304, Label: None, Status: loading
GPU: 1x RTX 4070, vCPUs: 24, RAM: 62.6 GB, Storage: 72.5 GB
Price: $0.020/hr, Image: dizcza/docker-hashcat:cuda
Net Up: 874.4 Mbps, Net Down: 873.0 Mbps
------------------------------------------------------------
```

Give your instance a more friendly (and easier to manage) name with labels :

```bash
└─$ python3 vastcontrol.py --rename 12741302 --to HelloGithub
Instance 12741302 renamed to HelloGithub.
```

Easily adds your public ssh key automatically to your instance and gives you the information you need to log in quickly :

```bash
└─$ python3 vastcontrol.py --label HelloGithub2 --add-ssh
SSH key added to instance with label HelloGithub2.
Connect to the instance with the following command :

ssh -p 40303 root@141.195.16.189 -L 8080:localhost:8080

```

Destroy your instance by its label name

```bash
└─$ python3 vastcontrol.py --delete HelloGithub2    
Instance 12741303 with label HelloGithub2 deleted.
```


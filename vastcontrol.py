import subprocess
import json
import argparse
from vastai import VastAI
import os

def run_vast_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error during command execution: {result.stderr}")
        return None
    return result.stdout

def list_instances_with_details():
    command = ['vastai', 'show', 'instances', '--raw']
    output = run_vast_command(command)
    if output:
        instances = json.loads(output)
        for instance in instances:
            instance_id = instance.get('id', 'Unknown')
            status = instance.get('actual_status', 'Unknown')
            label = instance.get('label', 'None')
            num_gpu = instance.get('num_gpus', 'Unknown')
            gpu_model = instance.get('gpu_name', 'Unknown')
            vcpus = instance.get('cpu_cores', 'Unknown')
            ram = instance.get('cpu_ram', 'Unknown') / 1024 if instance.get('cpu_ram') else 'Unknown'
            storage = instance.get('disk_space', 'Unknown')
            price = instance.get('instance', {}).get('totalHour', 'Unknown')
            image = instance.get('image_uuid', 'Unknown')
            net_up = instance.get('inet_up', 'Unknown')
            net_down = instance.get('inet_down', 'Unknown')

            if label != 'None':
                label_str = f"\033[1;34m{label}\033[0m"
            else:
                label_str = label

            print(f"ID: {instance_id}, Label: {label_str}, Status: {status}")
            print(f"GPU: {num_gpu}x {gpu_model}, vCPUs: {vcpus}, RAM: {ram:.1f} GB, Storage: {storage:.1f} GB")
            print(f"Price: ${float(price):.3f}/hr, Image: {image}")
            print(f"Net Up: {net_up} Mbps, Net Down: {net_down} Mbps")
            print('-' * 60)

def add_ssh_to_instance_by_label(label, ssh_key):
    vast_sdk = VastAI(api_key='YOUR_API_KEY')
    
    command = ['vastai', 'show', 'instances', '--raw']
    output = run_vast_command(command)
    if output:
        instances = json.loads(output)
        for instance in instances:
            instance_id = instance.get('id', 'Unknown')
            status = instance.get('actual_status', 'Unknown')
            instance_label = instance.get('label', 'None')

            if isinstance(instance, dict) and instance_label == label and status == 'running':
                ssh_host = instance.get('public_ipaddr', 'Unknown')
                
                ssh_port = instance.get('ports', {}).get('22/tcp', [{}])[0].get('HostPort', 'Unknown')

                vast_sdk.attach_ssh(instance_id=instance_id, ssh_key=ssh_key)
                print(f"SSH key added to instance with label {label}.")

                ssh_command = f"ssh -p {ssh_port} root@{ssh_host} -L 8080:localhost:8080"
                print(f"Connect to the instance with the following command :\n\n{ssh_command}\n")
                return
    else:
        print("Error: Instances retrieved are in the wrong format.")
    
    print(f"No running instances with label {label} found.")



def rename_instance(instance_id, new_label):
    command = ['vastai', 'label', 'instance', str(instance_id), new_label]
    output = run_vast_command(command)
    if output:
        print(f"Instance {instance_id} renamed to {new_label}.")

def delete_instance_by_label(label):
    command = ['vastai', 'show', 'instances', '--raw']
    output = run_vast_command(command)
    if output:
        instances = json.loads(output)
        for instance in instances:
            if instance['label'] == label:
                instance_id = instance['id']
                delete_command = ['vastai', 'destroy', 'instance', str(instance_id)]
                delete_output = run_vast_command(delete_command)
                if delete_output:
                    print(f"Instance {instance_id} with label {label} deleted.")
                return
        print(f"No instances found with the label {label}.")

parser = argparse.ArgumentParser(description="Managing Vast.ai instances")
parser.add_argument('--list-up', action='store_true', help="List running instances and their specifications")
parser.add_argument('--rename', type=int, help="ID of instance to be renamed")
parser.add_argument('--to', type=str, help="New name for the instance")
parser.add_argument('--delete', type=str, help="Delete an instance by its label")
parser.add_argument('--label', type=str, help="Instance label for adding an SSH key")
parser.add_argument('--add-ssh', action='store_true', help="Adding an SSH key to an instance")

args = parser.parse_args()

if args.list_up:
    list_instances_with_details()
elif args.rename and args.to:
    rename_instance(args.rename, args.to)
elif args.delete:
    delete_instance_by_label(args.delete)
elif args.label and args.add_ssh:
    with open(os.path.expanduser('~/.ssh/id_rsa.pub'), 'r') as key_file:
        ssh_key = key_file.read()
    add_ssh_to_instance_by_label(args.label, ssh_key)
else:
    print("No valid arguments provided. Use --help to see options.")

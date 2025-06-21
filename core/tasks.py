# core/tasks.py
from celery import shared_task
from .models import OLTDevice, ONU
from netmiko import ConnectHandler # Example for Netmiko

@shared_task
def fetch_onu_status(onu_id):
    # This task will run in the background
    try:
        onu = ONU.objects.get(id=onu_id)
        olt = onu.olt
        
        device = {
            'device_type': olt.brand, # Netmiko device type
            'host': olt.ip_address,
            'username': olt.username,
            'password': olt.password,
            'secret': olt.password, # For enable mode if needed
        }
        
        with ConnectHandler(**device) as net_connect:
            # Example: Fetching ONU status for Huawei
            command = f"display ont info by-sn {onu.sn}" # Replace with actual command
            output = net_connect.send_command(command)
            
            # Parse output and update ONU object
            # Example parsing (highly simplified):
            if "online" in output.lower():
                onu.is_online = True
                onu.last_seen_online = timezone.now()
                onu.offline_since = None
            else:
                onu.is_online = False
                if onu.offline_since is None:
                    onu.offline_since = timezone.now()
            
            # Parse Rx/Tx power, etc.
            # onu.rx_power = parse_rx_power(output)
            # onu.tx_power = parse_tx_power(output)
            
            onu.save()
            print(f"Updated status for ONU {onu.sn}")
            
    except ONU.DoesNotExist:
        print(f"ONU with ID {onu_id} not found.")
    except Exception as e:
        print(f"Error fetching ONU status for {onu_id}: {e}")

@shared_task
def remove_onu_from_olt(onu_id):
    try:
        onu = ONU.objects.get(id=onu_id)
        olt = onu.olt

        device = {
            'device_type': olt.brand,
            'host': olt.ip_address,
            'username': olt.username,
            'password': olt.password,
            'secret': olt.password,
        }

        with ConnectHandler(**device) as net_connect:
            # IMPORTANT: Use the correct command for your OLT brand to remove ONU
            # Example for Huawei (may vary):
            command = f"config\ninterface gpon {onu.olt_port.replace('GPON', '')}\nundo ont add sn-mac {onu.sn}\ncommit\nquit"
            # Or simpler: undo ont {onu_id_on_olt}
            output = net_connect.send_config_set(command.split('\n'))
            
            if "success" in output.lower() or "completed" in output.lower():
                print(f"Successfully removed ONU {onu.sn} from OLT {olt.name}")
                onu.delete() # Remove from your DB after successful removal from OLT
            else:
                print(f"Failed to remove ONU {onu.sn} from OLT {olt.name}. Output: {output}")
                # You might want to log this failure or mark ONU as "removal_failed"
    except ONU.DoesNotExist:
        print(f"ONU with ID {onu_id} not found for removal.")
    except Exception as e:
        print(f"Error removing ONU {onu_id} from OLT: {e}")

# This task can be scheduled to run periodically
@shared_task
def periodic_onu_status_check():
    for onu in ONU.objects.all():
        fetch_onu_status.delay(onu.id)

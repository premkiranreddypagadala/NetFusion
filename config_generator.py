 """config_generator.py
 Read topology JSON and generate device configuration snippets using simple Python templates.
 Output folder: generated_configs/
 """
 import os, json
 from pathlib import Path

 TEMPLATES = {
     'arista': """
 hostname {name}
 !
 interface Management1
   ip address {mgmt_ip}/24
 !
 """",
     'cisco': """
 hostname {name}
!
 interface GigabitEthernet0/0
   ip address {mgmt_ip} 255.255.255.0
!
 """",
     'paloalto': """
 set deviceconfig system hostname {name}
 set deviceconfig system ip-address {mgmt_ip}
 """
 }

 def load_topology(path):
     with open(path) as f:
         return json.load(f)

 def generate_config_for_device(dev):
     vendor = dev.get('vendor', 'generic').lower()
     tpl = TEMPLATES.get(vendor)
     if tpl:
         return tpl.format(**dev)
     # generic fallback:
     return f"""# Generic device config for {dev['name']}
 hostname {dev['name']}
 management ip {dev['mgmt_ip']}
 """.strip()

 def main(topology_path='sample_topology.json', outdir='generated_configs'):
     os.makedirs(outdir, exist_ok=True)
     topo = load_topology(topology_path)
     for dev in topo.get('devices', []):
         cfg = generate_config_for_device(dev)
         fname = Path(outdir) / f"{dev['name']}.cfg"
         with open(fname, 'w') as f:
             f.write(cfg.strip() + '\n')
         print('Wrote', fname)

 if __name__ == '__main__':
     import argparse
     p = argparse.ArgumentParser(description='Generate simple configs from topology JSON')
     p.add_argument('--topo', default='sample_topology.json')
     p.add_argument('--outdir', default='generated_configs')
     args = p.parse_args()
     main(args.topo, args.outdir)

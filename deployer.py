"""deployer.py
Simulated deployer for Project NetFusion.
It 'deploys' generated config files to a local folder named 'deployed' to emulate pushing configs to devices.
This avoids requiring network/device libraries and is safe to run locally.
"""
import os, shutil
from pathlib import Path
import time

DEPLOY_DIR = Path('deployed')

def deploy_config(cfg_path, device_name):
    DEPLOY_DIR.mkdir(exist_ok=True)
    dest = DEPLOY_DIR / f"{device_name}.cfg"
    shutil.copy(cfg_path, dest)
    # write a timestamp
    with open(dest, 'a') as f:
        f.write(f"\n# Deployed at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    return dest

def main(generated_dir='generated_configs'):
    generated = Path(generated_dir)
    if not generated.exists():
        print('No generated configs found. Run config_generator.py first.')
        return
    for cfg in generated.glob('*.cfg'):
        device = cfg.stem
        d = deploy_config(cfg, device)
        print(f'Deployed {cfg.name} -> {d}')

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Simulate deployment of configs')
    p.add_argument('--src', default='generated_configs', help='Source folder with .cfg files')
    args = p.parse_args()
    main(args.src)

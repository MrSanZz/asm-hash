import os
import platform
import shutil
import subprocess
import sys

def find_local_bin():
    default_path = "/usr/local/bin"
    if os.path.isdir(default_path):
        return default_path
    # fallback jika tidak ada
    raise "/usr/bin"

def get_architecture():
    return platform.machine()

def get_os():
    return platform.system()

def main():
    print("=== ASM Installer ===")

    try:
        local_bin = find_local_bin()
        print(f"[INFO] Local bin found at: {local_bin}")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # Print working directory
    current_dir = os.getcwd()
    print(f"[PWD] Current directory: {current_dir}")

    # Get architecture and OS
    arch = get_architecture()
    os_name = get_os()
    print(f"[INFO] Detected OS: {os_name}")
    print(f"[INFO] Detected architecture: {arch}")

    try:
        if arch == "x86_64" and os_name == "Linux":
            src = os.path.join(current_dir, "asm")
        elif arch in ["aarch64", "arm64"] or "Android" in os_name:
            src = os.path.join(current_dir, "asm_aarch64")
        else:
            print("[ERROR] Unsupported architecture or OS.")
            sys.exit(1)

        dest = os.path.join(local_bin, "asm")

        # Copy file
        shutil.copyfile(src, dest)
        os.chmod(dest, 0o755)  # Make it executable
        print(f"[SUCCESS] {os.path.basename(src)} installed to {dest}")

    except Exception as e:
        print(f"[ERROR] Failed to install ASM binary: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

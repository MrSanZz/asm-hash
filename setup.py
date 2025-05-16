import os
import platform
import shutil
import sys
import zipfile

def find_local_bin():
    default_path = "/usr/local/bin"
    if os.path.isdir(default_path):
        return default_path
    # fallback jika tidak ada
    return "/data/data/com.termux/files/usr/bin"

def get_architecture():
    return platform.machine()

def get_os():
    return platform.system()

def install_asm(local_bin, arch, os_name):
    if arch == "x86_64" and os_name == "Linux":
        src = os.path.join(os.getcwd(), "asm")
    elif arch in ["aarch64", "arm64"] or "Android" in os_name:
        src = os.path.join(os.getcwd(), "asm_aarch64")
    else:
        print("[ERROR] Unsupported architecture or OS.")
        return

    dest = os.path.join(local_bin, "asm")
    shutil.copyfile(src, dest)
    os.chmod(dest, 0o755)
    print(f"[SUCCESS] Installed {os.path.basename(src)} to {dest}")

def unzip_and_move_build(local_bin):
    zip_path = os.path.join(os.getcwd(), "builds.zip")
    extract_dir = os.path.join(os.getcwd(), "builds")

    if not os.path.exists(zip_path):
        print("[WARNING] builds.zip not found, skipping unzip.")
        return

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall()
            print("[INFO] Extracted builds.zip.")

        # Rename folder builds -> build
        build_src = os.path.join(os.getcwd(), "builds")
        build_renamed = os.path.join(os.getcwd(), "build")
        if os.path.exists(build_renamed):
            shutil.rmtree(build_renamed)
        os.rename(build_src, build_renamed)

        # Move to /usr/local/bin/build
        build_dest = os.path.join(local_bin, "build")
        if os.path.exists(build_dest):
            shutil.rmtree(build_dest)
        shutil.move(build_renamed, build_dest)
        print(f"[SUCCESS] Moved build folder to {build_dest}")

    except Exception as e:
        print(f"[ERROR] Failed to handle builds.zip: {e}")

def main():
    print("=== ASM + Build Installer ===")

    try:
        local_bin = find_local_bin()
        print(f"[INFO] Local bin path: {local_bin}")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print(f"[PWD] Current working directory: {os.getcwd()}")

    arch = get_architecture()
    os_name = get_os()
    print(f"[INFO] Detected OS: {os_name}")
    print(f"[INFO] Detected architecture: {arch}")

    # Install ASM
    install_asm(local_bin, arch, os_name)

    # Handle builds.zip → build → move
    unzip_and_move_build(local_bin)

if __name__ == "__main__":
    main()

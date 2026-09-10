import os
import shutil
import sys
import time

# ==================== CONFIGURATION ====================
SOURCE_DIR = r"C:\Users\whynew.in\OneDrive\Documents\MyProject"
BACKUP_DESTINATION_DIR = r"C:\Users\whynew.in\OneDrive\Documents\MyBackups"
# =======================================================


def execute_backup():
    if not os.path.exists(SOURCE_DIR):
        print(
            f"[ERROR] Source directory '{SOURCE_DIR}' does not exist.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not os.path.exists(BACKUP_DESTINATION_DIR):
        os.makedirs(BACKUP_DESTINATION_DIR)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    folder_name = os.path.basename(os.path.normpath(SOURCE_DIR))
    backup_filename = f"backup_{folder_name}_{timestamp}"
    local_archive_path = os.path.join(BACKUP_DESTINATION_DIR, backup_filename)

    print("=" * 60)
    print("                STARTING AUTOMATED BACKUP               ")
    print("=" * 60)

    try:
        final_path = shutil.make_archive(
            local_archive_path, "zip", root_dir=SOURCE_DIR
        )
        print(f"[SUCCESS] Archive created securely at: {final_path}")
        print("-" * 60)
        print("SUMMARY REPORT: BACKUP OPERATION COMPLETED SUCCESSFULLY")
    except Exception as e:
        print(f"[CRITICAL FAILURE] Compressing folder failed: {e}")
        print("-" * 60)
        print("SUMMARY REPORT: BACKUP OPERATION FAILED")
    print("=" * 60)


if __name__ == "__main__":
    execute_backup()

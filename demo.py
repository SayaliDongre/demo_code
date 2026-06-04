import os
import re

# IMPORTANT: Update this to the path of your SCRFD folder
SCRFD_DIR = r"C:\Users\sayalid\OneDrive - Godrej & Boyce Mfg. Co. Ltd\2D Face recognition\2D FACE DETECTION\SCRFD"

def fix_numpy_files():
    patched_count = 0
    for root, dirs, files in os.walk(SCRFD_DIR):
        for file in files:
            if not file.endswith(".py"):
                continue
                
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Automatically find and replace the deprecated numpy types
            # Regex ensures we don't accidentally turn np.int32 into np.int3232
            new_content = re.sub(r'np\.int(?!\d)', 'np.int32', content)
            new_content = re.sub(r'np\.float(?!\d)', 'np.float32', new_content)
            new_content = re.sub(r'np\.bool(?!\w)', 'bool', new_content)
            
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed: {file}")
                patched_count += 1
                
    print(f"\nDone! Successfully patched {patched_count} files.")

if __name__ == "__main__":
    fix_numpy_files()

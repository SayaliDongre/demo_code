import os

# Update this path if your dataset is located somewhere else on your laptop
BASE_DIR = r"C:\path\to\your\IR Dataset\images"

def clean_filenames():
    for folder in ["train", "val"]:
        folder_path = os.path.join(BASE_DIR, folder)
        
        if not os.path.exists(folder_path):
            print(f"Skipping {folder} - folder not found at {folder_path}")
            continue
            
        for filename in os.listdir(folder_path):
            # Check if the filename contains spaces or parentheses
            if " " in filename or "(" in filename or ")" in filename:
                
                # Replace spaces and parentheses with underscores
                clean_name = filename.replace(" ", "_").replace("(", "").replace(")", "")
                
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, clean_name)
                
                os.rename(old_path, new_path)
                print(f"Renamed: '{filename}' -> '{clean_name}'")

    print("\nAll filenames cleaned successfully!")

if __name__ == "__main__":
    clean_filenames()

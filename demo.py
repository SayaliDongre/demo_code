import os
import cv2

def convert_yolo_to_widerface(data_dir, output_file):
    """
    Converts YOLO-Face formatted annotations (normalized, per-image) 
    to WiderFace format (absolute, single file) for SCRFD training.
    Assumes images and .txt labels are in the SAME directory (`data_dir`).
    """
    # Create the directory for the output file if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    
    valid_extensions = ('.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG')
    
    converted_count = 0
    with open(output_file, 'w') as out_f:
        # Sort files to ensure deterministic ordering
        for filename in sorted(os.listdir(data_dir)):
            if not filename.endswith(valid_extensions):
                continue
                
            img_path = os.path.join(data_dir, filename)
            
            # Label is expected to be in the same folder with the same name
            label_filename = os.path.splitext(filename)[0] + '.txt'
            label_path = os.path.join(data_dir, label_filename)
            
            if not os.path.exists(label_path):
                print(f"Warning: No label found for {filename}, skipping.")
                continue
                
            # Read image to get absolute dimensions
            img = cv2.imread(img_path)
            if img is None:
                print(f"Warning: Could not read image {img_path}, skipping.")
                continue
                
            h_img, w_img, _ = img.shape
            
            # Write image header (SCRFD dataloader will join this with your image prefix path)
            out_f.write(f"# {filename}\n")
            
            with open(label_path, 'r') as in_f:
                for line in in_f:
                    parts = line.strip().split()
                    if len(parts) < 15:
                        continue
                    
                    # YOLO format: class cx cy w h x1 y1 x2 y2 x3 y3 x4 y4 x5 y5
                    # Values are normalized [0, 1]
                    cx, cy, w, h = map(float, parts[1:5])
                    
                    # Convert to absolute pixels
                    abs_w = w * w_img
                    abs_h = h * h_img
                    abs_cx = cx * w_img
                    abs_cy = cy * h_img
                    
                    # Convert center coordinates to top-left (xmin, ymin)
                    xmin = abs_cx - (abs_w / 2)
                    ymin = abs_cy - (abs_h / 2)
                    
                    # Bounding box format: xmin ymin w h
                    line_out = f"{xmin:.2f} {ymin:.2f} {abs_w:.2f} {abs_h:.2f}"
                    
                    # Landmarks (5 points)
                    for i in range(5):
                        lx = float(parts[5 + i*2]) * w_img
                        ly = float(parts[5 + i*2 + 1]) * h_img
                        # SCRFD expects EXACTLY 10 landmark values (x y only, NO visibility flags!)
                        line_out += f" {lx:.2f} {ly:.2f}"
                        
                    # Write the converted annotation line
                    out_f.write(line_out + "\n")
            
            converted_count += 1

    print(f"[{converted_count} images] Conversion complete! Saved to: {output_file}")


if __name__ == "__main__":
    # =========================================================
    # HARDCODED PATHS - Update BASE_DIR if it's located elsewhere
    # =========================================================
    BASE_DIR = "/home/aiml/sayali/VDB_Models/IR Dataset/images"
    
    TRAIN_DIR = os.path.join(BASE_DIR, "train")
    VAL_DIR = os.path.join(BASE_DIR, "val")
    
    # We will output the 'label.txt' directly inside the train and val folders
    TRAIN_OUT = os.path.join(TRAIN_DIR, "label.txt")
    VAL_OUT = os.path.join(VAL_DIR, "label.txt")
    
    print("--- Processing Train Dataset ---")
    if os.path.exists(TRAIN_DIR):
        convert_yolo_to_widerface(TRAIN_DIR, TRAIN_OUT)
    else:
        print(f"Error: Train directory not found at: {TRAIN_DIR}")
        
    print("\n--- Processing Val Dataset ---")
    if os.path.exists(VAL_DIR):
        convert_yolo_to_widerface(VAL_DIR, VAL_OUT)
    else:
        print(f"Error: Val directory not found at: {VAL_DIR}")

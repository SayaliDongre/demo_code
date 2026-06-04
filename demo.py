import os
import cv2

# Update this path if your dataset is located somewhere else on your laptop
BASE_DIR = r"C:\path\to\your\IR Dataset\images"

def convert_yolo_to_widerface():
    for folder in ["train", "val"]:
        data_dir = os.path.join(BASE_DIR, folder)
        if not os.path.exists(data_dir): 
            continue
            
        output_file = os.path.join(data_dir, "label.txt")
        converted_count = 0
        
        with open(output_file, 'w') as out_f:
            for filename in sorted(os.listdir(data_dir)):
                if not filename.lower().endswith(('.jpg', '.jpeg', '.png')): 
                    continue
                
                label_filename = os.path.splitext(filename)[0] + '.txt'
                label_path = os.path.join(data_dir, label_filename)
                
                if not os.path.exists(label_path): 
                    continue
                
                img = cv2.imread(os.path.join(data_dir, filename))
                if img is None: 
                    continue
                h_img, w_img, _ = img.shape
                
                # Write the image name header
                out_f.write(f"# {filename}\n")
                
                with open(label_path, 'r') as in_f:
                    for line in in_f:
                        parts = line.strip().split()
                        if len(parts) < 15: 
                            continue
                        
                        cx, cy, w, h = map(float, parts[1:5])
                        abs_w = w * w_img
                        abs_h = h * h_img
                        abs_cx = cx * w_img
                        abs_cy = cy * h_img
                        
                        xmin = abs_cx - (abs_w / 2)
                        ymin = abs_cy - (abs_h / 2)
                        
                        # 1. Start with the 4 bounding box values
                        line_out = f"{xmin:.2f} {ymin:.2f} {abs_w:.2f} {abs_h:.2f}"
                        
                        # 2. Add the 15 landmark values
                        for i in range(5):
                            lx = float(parts[5 + i*2]) * w_img
                            ly = float(parts[5 + i*2 + 1]) * h_img
                            line_out += f" {lx:.2f} {ly:.2f} 0.0"
                            
                        # 3. Add EXACTLY ONE dummy score at the end (outside the loop!)
                        line_out += " 1.0"
                        
                        # Write the perfect 20-element line
                        out_f.write(line_out + "\n")
                
                converted_count += 1

        print(f"[{converted_count} images] Conversion complete for {folder}! Saved to: {output_file}")

if __name__ == "__main__":
    convert_yolo_to_widerface()

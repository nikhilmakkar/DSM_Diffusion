import os
import glob
from pathlib import Path

def create_image_pairs_file(output_file):
    # Find all county directories in indiana folder
    indiana_dir = "./indiana"
    counties = [d for d in os.listdir(indiana_dir) if os.path.isdir(os.path.join(indiana_dir, d))]
    print(f"Found counties: {counties}")
    
    pairs_count = 0
    with open(output_file, 'w') as f:
        for county in counties:
            # Construct paths for ortho and dsm directories
            ortho_dir = os.path.join(indiana_dir, county, "ortho")
            dsm_dir = os.path.join(indiana_dir, county, "dsm")
            
            if not (os.path.exists(ortho_dir) and os.path.exists(dsm_dir)):
                continue
                
            # Get all ortho files
            ortho_pattern = os.path.join(ortho_dir, "patch_*.png")  # Matches patch_0.png, patch_100.png, etc.
            ortho_files = sorted(glob.glob(ortho_pattern), 
                               key=lambda x: int(x.split('patch_')[1].split('.png')[0]))  # Sort numerically
            
            for ortho_path in ortho_files:
                # Get the patch number from ortho filename
                patch_num = os.path.basename(ortho_path).split('patch_')[1].split('.png')[0]
                
                # Construct corresponding dsm path
                dsm_path = os.path.join(dsm_dir, f"patch_{patch_num}.png")
                
                # Check if dsm file exists
                if os.path.exists(dsm_path):
                    # Convert to relative paths starting from indiana/
                    ortho_relative = os.path.join("indiana", county, "ortho", f"patch_{patch_num}.png")
                    dsm_relative = os.path.join("indiana", county, "dsm", f"patch_{patch_num}.png")
                    
                    # Convert to forward slashes and write to file
                    ortho_relative = ortho_relative.replace('\\', '/')
                    dsm_relative = dsm_relative.replace('\\', '/')
                    
                    f.write(f"{ortho_relative} {dsm_relative}\n")
                    pairs_count += 1
    
    print(f"Total pairs found and written: {pairs_count}")

# Example usage
output_file = "image_pairs.txt"
create_image_pairs_file(output_file)
import rasterio
import numpy as np
from pathlib import Path
import cv2
from tqdm import tqdm
import os

def create_patches(ortho_path, dsm_path, output_dir, patch_size=512, bands=[0,1,2]):
    """
    Create corresponding patches from ortho and DSM TIF files.
    
    Args:
        ortho_path (str): Path to the ortho TIF file
        dsm_path (str): Path to the DSM TIF file
        output_dir (str): Directory to save patches
        patch_size (int): Size of patches (default: 512)
        bands (list): List of bands to use from ortho image (default: [0,1,2] for RGB)
    """
    # Create output directories
    output_dir = Path(output_dir)
    ortho_out_dir = output_dir / 'ortho_patches'
    dsm_out_dir = output_dir / 'dsm_patches'
    
    for dir_path in [ortho_out_dir, dsm_out_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Open both files
    with rasterio.open(ortho_path) as ortho_src, rasterio.open(dsm_path) as dsm_src:
        # Get the intersection of both rasters' bounds
        ortho_bounds = ortho_src.bounds
        dsm_bounds = dsm_src.bounds
        
        intersection_bounds = (
            max(ortho_bounds.left, dsm_bounds.left),
            max(ortho_bounds.bottom, dsm_bounds.bottom),
            min(ortho_bounds.right, dsm_bounds.right),
            min(ortho_bounds.top, dsm_bounds.top)
        )
        
        # Calculate window for the intersection
        ortho_window = rasterio.windows.from_bounds(*intersection_bounds, transform=ortho_src.transform)
        dsm_window = rasterio.windows.from_bounds(*intersection_bounds, transform=dsm_src.transform)
        
        # Read the data
        ortho_data = ortho_src.read(window=ortho_window)
        dsm_data = dsm_src.read(1, window=dsm_window)  # Read only first band for DSM
        
        # Get DSM metadata for scaling
        # dsm_min = dsm_data.min()
        # dsm_max = dsm_data.max()
        
        # Select specified bands from ortho
        ortho_data = ortho_data[bands]
        
        # Get dimensions
        _, height, width = ortho_data.shape
        
        # Calculate number of patches
        n_patches_h = height // patch_size
        n_patches_w = width // patch_size
        
        print(f"Will generate {n_patches_h * n_patches_w} patches per image")
        
        # Generate patches
        patch_count = 0
        for i in tqdm(range(n_patches_h)):
            for j in range(n_patches_w):
                # Extract patches
                h_start = i * patch_size
                w_start = j * patch_size
                
                ortho_patch = ortho_data[:, h_start:h_start+patch_size, 
                                       w_start:w_start+patch_size]
                dsm_patch = dsm_data[h_start:h_start+patch_size, 
                                   w_start:w_start+patch_size]
                
                # Check for invalid patches
                if (np.isnan(ortho_patch).any() or np.isnan(dsm_patch).any() or
                    np.all(ortho_patch == 0) or np.all(dsm_patch == 0)):
                    continue
                
                # Transpose ortho patch for correct channel order
                ortho_patch = np.transpose(ortho_patch, (1, 2, 0))
                
                # Save ortho patch
                cv2.imwrite(
                    str(ortho_out_dir / f'patch_{patch_count}.png'),
                    cv2.cvtColor(ortho_patch, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
                )
                
                # Save DSM patch as 16-bit PNG to preserve precision
                # Convert to 16-bit unsigned int for PNG storage
                # Save actual min/max values in filename for later reconstruction

                dsm_filename = f'patch_{patch_count}.png'
                dsm_ft_patch = dsm_patch * 3.2808 # for dc area
                # cv2.imwrite(
                #     str(dsm_out_dir / dsm_filename),
                #     dsm_patch.astype(np.float32)
                #     # dsm_patch.astype(np.uint16)
                # )
                cv2.imwrite(
                    str(dsm_out_dir / dsm_filename),
                    dsm_ft_patch.astype(np.uint16)
                 
                )
                
                patch_count += 1
        
        print(f"Successfully generated {patch_count} valid patches")

def main():
    # Example usage
    ortho_path = 'ortho_dc.tif'
    dsm_path = 'dsm_dc.tif'
    output_dir = 'output'
    
    create_patches(
        ortho_path=ortho_path,
        dsm_path=dsm_path,
        output_dir=output_dir,
        patch_size=512,
        bands=[0, 1, 2]  # RGB bands
    )

if __name__ == "__main__":
    main()
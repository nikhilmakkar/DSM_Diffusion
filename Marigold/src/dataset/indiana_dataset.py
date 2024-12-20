# Last modified: 2024-02-08
#
# Copyright 2023 Bingxin Ke, ETH Zurich. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------
# If you find this code useful, we kindly ask you to cite our paper in your work.
# Please find bibtex at: https://github.com/prs-eth/Marigold#-citation
# If you use or adapt this code, please attribute to https://github.com/prs-eth/marigold.
# More information about the method can be found at https://marigoldmonodepth.github.io
# --------------------------------------------------------------------------

# from .base_depth_dataset import BaseDepthDataset, DepthFileNameMode


# class ScanNetDataset(BaseDepthDataset):
#     def __init__(
#         self,
#         **kwargs,
#     ) -> None:
#         super().__init__(
#             # ScanNet data parameter
#             min_depth=1e-3,
#             max_depth=10,
#             has_filled_depth=False,
#             name_mode=DepthFileNameMode.id,
#             **kwargs,
#         )

#     def _read_depth_file(self, rel_path):
#         depth_in = self._read_image(rel_path)
#         # Decode ScanNet depth
#         depth_decoded = depth_in / 1000.0
#         return depth_decoded

from .base_depth_dataset import BaseDepthDataset, DepthFileNameMode
import numpy as np

class IndianaDataset(BaseDepthDataset):
    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(
            # Your dataset parameters
            min_depth=0,
            max_depth=1500,
            has_filled_depth=False,
            name_mode=DepthFileNameMode.id,
            **kwargs,
        )

    def _read_depth_file(self, rel_path):
        # Convert DSM path from ortho path
        depth_in = self._read_image(rel_path)
        
        # Since all channels are same, take just one channel
        # Assuming depth_in is (H, W, 3)
        # depth_single = depth_in[:, :, 0]  # Take first channel
        depth_single  = depth_in
        
        return depth_single  # Will return (H, W) with values 0-255
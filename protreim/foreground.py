from PIL import Image
import cv2
import numpy as np
import numpy.typing as npt

from protreim.typing import Color

def extract_foreground(
    im: Image.Image, 
    background_color: Color,
    grabcut_iter_count: int = 5,
    boundary_fore: int = 90, 
    boundary_back: int = 160
) -> Image.Image:
    """ Extract foreground of image.

    Parameters
    ----------
    im : PIL.Image.Image
        Target image.
    background_color : Color
        Background color.
    grabcut_iter_count : int
        Number of iteration of GrabCut algorithm.

    Returns
    -------
    PIL.Image.Image
        Extracted forground image.
    """
    im_array: npt.NDArray[np.int64] = np.array(im, dtype=np.uint8)
    gaussian: npt.NDArray[np.int64] = cv2.GaussianBlur(im_array, (5, 5), 0)
    hsv: npt.NDArray[np.int64] = cv2.cvtColor(gaussian, cv2.COLOR_RGB2HSV)

    # edge検出で反射部分を検出
    gray = cv2.cvtColor(gaussian, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.medianBlur(gray, 3)
    gray_filtered = cv2.bilateralFilter(gray_blur, 7, 75, 75)
    canny = cv2.Canny(gray_filtered, 50, 100)
    closing = cv2.morphologyEx(
        cv2.medianBlur(canny, 3), 
        cv2.MORPH_CLOSE, 
        np.ones((3, 3), np.uint8), 
        iterations=10
    )
    
    
    # foreground mask
    tmp_mask = cv2.inRange(
        hsv,
        np.array([0, 0, 0]),
        np.array([180, 255, boundary_fore])
    )
    foreground_mask: npt.NDArray[np.uint8] = np.where(
        tmp_mask == 0, 
        cv2.GC_BGD, # GC_BGD 明らかな背景ピクセル．
        cv2.GC_FGD  # GC_FGD 明らかな前景（物体）ピクセル．
    ).astype(np.uint8) 

    # pr-foreground mask
    tmp_mask = cv2.inRange(
        hsv,
        np.array([0, 0, boundary_fore]),
        np.array([180, 255, boundary_back])
    )
    pr_foreground_mask: npt.NDArray[np.uint8] = np.where(
        tmp_mask == 0, 
        cv2.GC_BGD, 
        cv2.GC_PR_FGD  # GC_PR_FGD 前景かもしれないピクセル．
    ).astype(np.uint8)

    # pr-background mask
    tmp_mask = cv2.inRange(
        hsv,
        np.array([0, 0, boundary_back]),
        np.array([180, 255, 255])
    )
    pr_background_mask: npt.NDArray[np.uint8] = np.where(
        tmp_mask == 0, 
        cv2.GC_BGD, 
        cv2.GC_PR_BGD  # GC_PR_BGD 背景かもしれないピクセル．
    ).astype(np.uint8)

    mask: npt.NDArray[np.uint8] = foreground_mask | pr_foreground_mask | pr_background_mask
    mask = np.where(closing == 255, cv2.GC_PR_FGD, mask)

    cv2.grabCut(
        im_array,
        mask,
        (0, 0, *mask.shape),
        np.zeros((1, 65), np.float64),
        np.zeros((1, 65), np.float64),
        grabcut_iter_count,
        cv2.GC_INIT_WITH_MASK,
    )

    mask = np.where((mask == cv2.GC_BGD)|(mask == cv2.GC_PR_BGD), cv2.GC_BGD, cv2.GC_FGD)

    background = Image.new('RGB', im.size, color=background_color)
    im_array[mask == 0] = np.array(background)[0, 0, :]
    return Image.fromarray(im_array)
# -*- coding: utf-8 -*-
"""
Helper functions to manage external files.
"""

from   os          import path as op
from   functools   import wraps
# -*- coding: utf-8 -*-
"""
Miscellaneous functions to process different types of files.
"""
from itertools import product

import nibabel as nib
import numpy   as np

from boyle.nifti.read import read_img


def get_bounding_box(in_file):
    """
    Retrieve the bounding box of a volume in millimetres.
    """
    img = nib.load(in_file)

    # eight corners of the 3-D unit cube [0, 0, 0] .. [1, 1, 1]
    corners = np.array(list(product([0, 1], repeat=3)))
    # scale to the index range of the volume
    corners = corners * (np.array(img.shape[:3]) - 1)
    # apply the affine transform
    corners = img.affine.dot(np.hstack([corners, np.ones((8, 1))]).T).T[:, :3]

    # get the extents
    low_corner  = np.min(corners, axis=0)
    high_corner = np.max(corners, axis=0)

    return [low_corner.tolist(), high_corner.tolist()]


def niftiimg_out(f):
    """ Picks a function whose first argument is an `img`, processes its
    data and returns a numpy array. This decorator wraps this numpy array
    into a nibabel.Nifti1Image."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        r = f(*args, **kwargs)

        img = read_img(args[0])
        return nib.Nifti1Image(r, affine=img.get_affine(), header=img.header)

    return wrapped


def get_extension(filepath, check_if_exists=False, allowed_exts=None):
    """Return the extension of filepath.

    Parameters
    ----------
    filepath: string
        File name or path

    check_if_exists: bool

    allowed_exts: dict
        Dictionary of strings, where the key if the last part of a complex ('.' separated) extension
        and the value is the previous part.
        For example: for the '.nii.gz' extension I would have a dict as {'.gz': '.nii'}
        Default: {'.gz': '.nii'}

    Returns
    -------
    ext: str
        The extension of the file name or path
    """
    if allowed_exts is None:
        allowed_exts = {'.gz': '.nii'}

    try:
        rest, ext = op.splitext(filepath)
        if ext in allowed_exts:
            alloweds = allowed_exts[ext]
            _, ext2 = op.splitext(rest)
            if ext2 in alloweds:
                ext = ext2 + ext
    except:
        raise
    else:
        return ext


def add_extension_if_needed(filepath, ext):
    """Add the extension ext to fpath if it doesn't have it.

    Parameters
    ----------
    filepath: str
        File name or path

    ext: str
        File extension

    Returns
    -------
    filepath: str
        File name or path with extension added, if needed.
    """
    if not filepath.endswith(ext):
        filepath += ext

    return filepath


def remove_ext(filepath):
    """Removes the extension of the file.

    Parameters
    ----------
    filepath: str
        File path or name

    Returns
    -------
    filepath: str
        File path or name without extension
    """
    return filepath[:filepath.rindex(get_extension(filepath))]
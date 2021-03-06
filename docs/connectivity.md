
# Resting-state fMRI connectivity analysis
**This pipeline is under development.**

This pipeline would need to warp an atlas file with the fMRI image, and then
perform the connectivity measures.
There is already an interface almost done in [`pypes.interfaces.nilearn.connectivity`](https://github.com/Neurita/pypes/blob/master/pypes/interfaces/nilearn/connectivity.py) for this.

##### Related settings
```yaml
normalize_atlas: True
atlas_file: ''

# RS-fMRI CONNECTIVITY
## if atlas_file is defined, perform connectivity analysis
rest_preproc.connectivity: True
## if further smoothing (remember the output of the rest workflow is already smoothed)
rest_connectivity.standardize: False
rest_connectivity.kind: correlation # choices: "correlation", "partial correlation", "tangent", "covariance", "precision".
rest_connectivity.smoothing_fwhm: 8
#rest_connectivity.resampling_target: # choices: "mask", "maps" or undefined.
rest_connectivity.atlas_type: labels # choices: "labels", "probabilistic".
```


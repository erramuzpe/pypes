# -*- coding: utf-8 -*-

from .environ import  spm_tpm_priors_path

from .files   import  (remove_ext,
                       get_extension,
                       get_bounding_box)

from .piping  import  (extend_trait_list,
                       fsl_merge,
                       joinstrings,
                       find_wf_node,
                       get_datasink,
                       get_input_node)
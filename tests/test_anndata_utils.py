import tempfile

import anndata
import numpy as np
import pandas as pd
import cellarr.utils_anndata
import pytest
import tiledb
import cellarr

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def test_consolidate_symbols():
    np.random.seed(1)

    n = 100
    y = np.eye(n, dtype=int)
    gene_index = [f"gene_{(i % 10)+1}" for i in range(n)]
    cmat, groups = cellarr.utils_anndata.consolidate_duplicate_symbols(
        y, gene_index, consolidate_duplicate_gene_func=sum
    )

    assert len(groups) == 10
    assert cmat.shape[1] == 10
    assert cmat[:, 1].sum() == 10


def test_remap_anndata():
    np.random.seed(1)

    n = 100
    y = np.eye(n, dtype=int)
    gene_index = [f"gene_{(i % 10)+1}" for i in range(n)]

    var_df = pd.DataFrame({"names": gene_index}, index=gene_index)
    obs_df = pd.DataFrame({"cells": [f"cell1_{j+1}" for j in range(n)]})
    adata = anndata.AnnData(layers={"counts": y}, var=var_df, obs=obs_df)

    cmat = cellarr.utils_anndata.remap_anndata(adata, {"gene_1": 0, "gene_2": 1})

    assert cmat.shape == (100, 2)
    assert len(cmat.data) != 0

    # test with no matching gene symbols should give me a
    # 0 size data array
    cmat = cellarr.utils_anndata.remap_anndata(
        adata, {"gene_10000": 0, "gene_20000": 1}
    )

    assert cmat.shape == (100, 2)
    assert len(cmat.data) == 0

    # test with empty array
    cmat = cellarr.utils_anndata.remap_anndata(adata, {})

    assert cmat.shape == (100, 0)
    assert len(cmat.data) == 0

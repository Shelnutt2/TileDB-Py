#%%

import numpy as np
import tiledb

from tiledb.tests.common import *

class DomainIndexingTest(DiskTestCase):

    def test_fp_domain_indexing(self):
        array_path = self.path("test_domain_idx")


        # test case from https://github.com/TileDB-Inc/TileDB-Py/issues/201
        tile = 1
        dom = tiledb.Domain(tiledb.Dim(name="x", domain=(-89.75, 89.75), tile=tile, dtype=np.float64),
                            tiledb.Dim(name="y", domain=(-179.75, 179.75), tile=tile, dtype=np.float64),
                            tiledb.Dim(name="z", domain=(157498, 157863), tile=tile, dtype=np.float64)
                            )
        schema = tiledb.ArraySchema(domain=dom, sparse=True,
                                    attrs=[tiledb.Attr(name="data", dtype=np.float64)])

        tiledb.SparseArray.create(array_path, schema)

        # fake data
        X = np.linspace(*(-89.75, 89.75), 359)
        Y = np.linspace(*(-179.75, 179.75), 359)
        Z = np.linspace(*(157498, 157857), 359)

        #data = np.random.rand(*map(lambda x: x[0], (X.shape, Y.shape, Z.shape)))
        data = np.random.rand(X.shape[0])

        with tiledb.SparseArray(array_path, mode='w') as A:
            A[X, Y, Z] = data

        with tiledb.SparseArray(array_path) as A:

            # check direct slicing
            assert_array_equal(
                A.domain_index[ X[0], Y[0], Z[0] ]['data'],
                data[0])

            # check small slice ranges
            tmp = A.domain_index[
                X[0] : np.nextafter(X[0], 0), Y[0] : np.nextafter(Y[0], 0), Z[0] : np.nextafter(Z[0], Z[0] + 1)
                ]
            assert_array_equal(
                tmp['data'],
                data[0]
            )

            # check slicing last element
            tmp = A.domain_index[ X[-1], Y[-1], Z[-1] ]
            assert_array_equal(
                tmp['data'],
                data[ -1 ]
            )

            # check slice range multiple components
            tmp = A.domain_index[ X[1]:X[2], Y[1]:Y[2], Z[1]:Z[2] ]
            assert_array_equal(
                tmp['data'],
                data[1:3]
            )

            # check an interior point
            coords = X[145], Y[145], Z[145]
            tmp = A.domain_index[coords]
            assert_array_equal(
                tmp['coords'].view(np.float64),
                np.array(coords)
            )
            assert_array_equal(
                tmp['data'],
                data[145]
            )

            # check entire domain
            tmp = A.domain_index[X[0]:X[-1], Y[0]:Y[-1], Z[0]:Z[-1]]
            assert_array_equal(
                tmp['data'],
                data[:]
            )

            # check entire domain
            # TODO uncomment if vectorized indexing is available
            #coords = np.array([X,Y,Z]).transpose().flatten()
            #tmp = A.domain_index[coords]
            #assert_array_equal(
            #    tmp['data'],
            #    data[:]
            #)

import numpy as np
import warnings


def eitheriter(ab):
    a, b = ab
    return hasattr(a, '__iter__') or hasattr(b, '__iterb__')


def snap_to_edges(cube, theta, a, b):
    ret = theta
    if np.any(np.isclose(cube, 0)) or np.any(np.isclose(cube, 1)):
        for i in range(len(cube)):
            if np.isclose(cube[i], 0):
                ret[i] = a[i] if hasattr(a, '__iter__') else a
            elif np.isclose(cube[i], 1):
                ret[i] = b[i] if hasattr(b, '__iter__') else b
            else:
                pass
    return ret


def guard_against_inf_nan(cube, theta, logzero, loginf):
    ret = theta
    if not np.all(np.isfinite(ret)):
        for i in range(len(cube)):
            if np.isclose(cube[i], 0):
                ret[i] = logzero
            elif np.isclose(cube[i], 1):
                ret[i] = loginf
            elif not np.isfinite(ret[i]):
                ret[i] = logzero
            else:
                pass
    return ret


def process_stdev(stdev, mean, bounds):
    if isinstance(stdev, float):
        stdev = np.zeros(len(mean)) + stdev
    elif len(mean) != len(stdev):
        raise ValueError(
            'Proposal Mean and covariance are of incompatible lengths: ' +
            f'len(mean)={len(mean)} vs. len(stdev)={len(stdev)}')
    else:
        if len(stdev[0]) != len(mean):
            raise ValueError(
                'Dimensions of covariance and mean don\'t match' +
                f'len(stdev)={len(stdev)} vs len(mean)={len(mean)}')

    try:
        a, b = bounds
    except ValueError:
        a, b = bounds.T
        warnings.warn('Bounds should be transposed.')

    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        pass
    else:
        if len(a) != len(b):
            raise ValueError('Lopsided bounds: ' +
                             f'len(a)={len(a)} vs. len(b)={len(b)}')

        if 0 != len(a) != len(mean):
            raise ValueError(
                'Proposal mean and boundaries are of imcompatible lengths: ' +
                f'len(a)={len(a)} vs len(mean)={len(mean)}')

    return stdev, a, b

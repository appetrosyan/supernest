import anesthetic
import argparse
import sys
from itertools import takewhile, filterfalse
import numpy as np
from pprint import pformat

known_derived = {
    'As',
    'omegamh2',
    'DHBBN',
    's8h5',
    's8omegamp5',
    's8omegamp25',
    'A',
    'clamp'
}

ambiguous = {
    'H0',
    'omegam',
    'omega_de',
    'YHe',
    'Y_p',
    'zre',
    'sigma8',
    'rdrag',
    'age'
}

known_primary = {
    'ns',
    'logA',
    'theta_MC_100',
    'ombh2',
    'omch2',
    'tau'
}

def main(**ka):
    if ka['nested']:
        sa = anesthetic.NestedSamples(root=ka['nested'])
    elif ka['mcmc']:
        sa = anesthetic.MCMCSamples(root=ka['mcmc'])
    else:
        print('Provide input.')

    removed_pars = known_derived\
        .union(ambiguous)\
        .union(ka.pop('removed_params', {}))\
        .difference(ka.pop('kept_params', {}))
    cp, m, cv = params(sa, removed_pars)
    
    if ka['cobaya']:
        print(f'covmat_params: {cp}')
        print(f'mean: {pformat(m)}')
        print(f'covmat: {repr(cv)[6:-1]}')
    elif ka['supercosmo']:  
        raise NotImplementedError()
    else:
        for p, e in zip(cp, np.linalg.eigvals(cv)):
            print(f'{p}: {e}')


def params(samples, removed_params):
    covmat_params = [x for x in filterfalse
                     (lambda y: y in removed_params,
                      takewhile(lambda s: not samples[s].name.startswith('chi2_'),
                                samples))]
    
    mean = {x: samples[x].mean() for x in covmat_params}
    covmat = np.array([[samples[x].cov(samples[y])
                        for x in covmat_params] for y in covmat_params])
    return covmat_params, mean, covmat


def parse_arguments():
    d = 'Extract the covariance matrices as well as means in a' +\
        'structured input format, suitable for cobaya and supercosmochord'

    parser = argparse.ArgumentParser(description=d)
    in_kind = parser.add_mutually_exclusive_group()
    in_kind.add_argument('-n', '--nested',
                         help='nested samples\' `file_root`')
    in_kind.add_argument('-m', '--mcmc',
                         help='MCMC samples\' `file_root`')
    out_kind = parser.add_mutually_exclusive_group()
    out_kind.add_argument('-c', '--cobaya',
                          action='store_true',
                          help='output in the format acceptable by `cobaya`.')
    out_kind.add_argument('-s', '--supercosmo',
                          action='store_true',
                          help='output in the format acceptable by `superCosmoChord`.')
    parser.add_argument('-k', '--keep', metavar='kept_params',
                        nargs='+', type=str,
                        help='the parameters that should be kept, even if classified as derived.')
    parser.add_argument('-r', '--remove', metavar='removed_params',
                        nargs='+', type=str,
                        help='the parameters that should be excluded.')

    return parser.parse_args() 

if __name__ == '__main__':
    main(**vars(parse_arguments()))



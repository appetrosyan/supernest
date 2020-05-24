# SSPR

Stochastic superpositional posterior repartitioning used in conjunction with Bayesian inference engines such as PolyChord and MultiNest. 

# What is Bayesian inference

Bayesian inference is a suitable framework for model fitting. You give it a theory and some data and it tells you how well the theory fits the data, while also telling you what the theory's parameters should be for the fit to be the best.

# Installation

The preferred way is to use 
```
pip install sspr
```

though other packages will be developed as needed. 

If you know what you're doing you can clone this repository and install manually, using 

```
cd sspr && python3 setup.py
```

You also need to have either [PolyChord](https://github.com/PolyChord/PolyChordLite) or [MultiNest](https://github.com/farhanferoz/MultiNest) (or both) installed. 
# Usage


## Models and settings 
### Wrappers
This  package comes with thin wrappers around ``PolyChord`` and ``MultiNest``. Effort was put in, so that using our work is as easy as can be. 

To get started, just `import sspr.wrappers.polychord as sspc` and replace every instance of `polychord.run_polychord()` with  `sspc.run_polychord()`. This will give you effectively the same API as PolyChord (up to a search and replace), but with extra features. 

### Base model
If you're writing new code, you should subclass the ``sspr.models.BaseModel``, by implemeting a prior ``quantile`` a ``log_likelihood`` and as many ``proposals`` as you see fit. More on that later. 


## Defining proposals
A proposal can be defined in many ways, currently, the hardest way that offers the best performance is to define a proposal directly, by specifying its prior quantile and likelihood, (see paper (TODO) on how to do that). 

99% of all inferences with nested sampling use a uniform prior, and likely use a correlated Gaussian to communicate the proposal distribution. This case can be easily spcified: 
``` 
from sspr.proposals import UniGaussian 

...
def prior(cube):
    ...
    
def log_likelihood(theta):
    ...
    
proposal = UniGaussian(prior, log_likelihood, mu, cov)
sspc.run_polychord(..., proposal=proposal)
```
 
or if you're not using a wrapper, 

```
import sspr

sspr.nested_sample(model, proposal=proposal, sampler='PolyChord')
```
## Backends
The sampler will be chosen automatically depending on the settings, e.g. for higher number of dimensions it would be faster than MultiNest, because the average case time complexity of MultiNest is exponential, while PolyChord's is polynomial. However, if you need to force the use of a particular sampler, just use the variable sampler. 

This is true  even if you're using the wrappers. By default the sampler whose API is used is being preferred, but you can just as well use 

``` 
sspc.run_polychord(..., sampler='MultiNest')
```

to retain the settings, but use a different sampler.  

# What is this useful for 

Suppose that you were running a complex Bayesian inference, e.g. [Cobaya](https://cobaya.readthedocs.io/en/latest/). You have a choice of sampler, e.g. Monte-Carlo, Metropolis Hastings or you could choose to use Nested Sampling, among a family of other inference methods. If you choose the former, you get a good idea of what the model parameters should be quick, but you have no idea how good the fit is, because MCMC  and MH don't evaluate the evidence. You think to use Nested Sampling, but that takes too long, and you can't give it more information to run faster... At least not without this package. 

This is a thin wrapper around both PolyChord and Multinest's code, that allows you to specify a proposal distribution. For now it's mainly a multivariate correlated Gaussian, but other distributions are being planned. 

## How much faster/more precise can this make inference? 

Our preliminary academic benchmarks showed a runtime reduction by a factor of 20. Your mileage may vary, but if you're willing to sacrifice some precision, you can make it go even faster. 

If you really want the extra precision, you can expect an uplift by two orders of magnitude, if you started with a uniform prior (as we often do in nested sampling) and used the posterior chains to generate the distribution. 


# License (WIP)
The program is dual licensed, the version here is: 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
Basically, you can use it, give it to anyone you want, and modify to your heart's content, as long as you give credit and don't narrow the license. You also shouldn't link against proprietary licensed software downstream. For example, you can safely run this on a Scientific Linux-running cluster, as long as you avoid programs that were compiled with intel's compilers. By choosing to use this library you get a speedup of about 2,000% so I would strongly encourage you to make the effort to use FOSS libraries. You can technically pass the information to a proprietary program if you really need to without violating GPLv3 as long as you don't dynamically link it against our code. 

Unfortunately, because MultiNest is not OpenSource, you cannot use sspr with MultiNest as a backend. Our API is flexible enough to default to PolyChord as a back-end and you don't need a rewrite on the front-end. In fact, if you wanted to try PolyChord, but were unable to because your code is for multinest, now you can do it.  

The other license is commercial. If you absolutely need to use some proprietary software downstream, we do have a license under different terms. Please contact me directly at a-p-petrosyan@yandex.ru. This will allow you to, for example, use MultiNest as a back-end as well as a front-end. 
# The trackintel framework


[![PyPI version](https://badge.fury.io/py/trackintel.svg)](https://badge.fury.io/py/trackintel)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/trackintel.svg)](https://anaconda.org/conda-forge/trackintel)
[![Actions Status](https://github.com/mie-lab/trackintel/workflows/Tests/badge.svg)](https://github.com/mie-lab/trackintel/actions?query=workflow%3ATests)
[![Documentation Status](https://readthedocs.org/projects/trackintel/badge/?version=latest)](https://trackintel.readthedocs.io/en/latest/?badge=latest)
[![codecov.io](https://codecov.io/gh/mie-lab/trackintel/coverage.svg?branch=master)](https://codecov.io/gh/mie-lab/trackintel)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![asv](http://img.shields.io/badge/benchmarked%20by-asv-green.svg?style=flat)](https://mie-lab.github.io/trackintel/)

*trackintel* is a library for the analysis of spatio-temporal tracking data with a focus on human mobility. The core of *trackintel* is the hierarchical data model for movement data that is used in GIS, transport planning and related fields. We provide functionalities for the full life-cycle of human mobility data analysis: import and export of tracking data of different types (e.g, trackpoints, check-ins, trajectories), preprocessing, data quality assessment, semantic enrichment, quantitative analysis and mining tasks, and visualization of data and results.
Trackintel is based on [Pandas](https://pandas.pydata.org/) and [GeoPandas](https://geopandas.org/#). 

You can find the documentation on the [trackintel documentation page](https://trackintel.readthedocs.io/en/latest). 

Try *trackintel* online in a MyBinder notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mie-lab/trackintel/HEAD?filepath=%2Fexamples%2Ftrackintel_basic_tutorial.ipynb)

Please star this repo and [cite](#citelink) our paper if you find our work is helpful for you.

## Data model

An overview of the data model of *trackintel*:
* **positionfixes** (Raw tracking points, e.g., GPS recordings or check-ins)
* **staypoints** (Locations where a user spent time without moving, e.g., aggregations of positionfixes or check-ins). Staypoints can be classified into the following categories:
  * **activity** staypoints. Staypoints with a purpose and a semantic label, e.g., stopping at a cafe to meet with friends or staying at the workplace.
  * non-activity staypoints. Staypoints without an explicit purpose, e.g., waiting for a bus or stopping in a traffic jam.
* **locations** (Important places that are visited more than once, e.g., home or work location)
* **triplegs** (or stages) (Continuous movement without changing mode, vehicle or stopping for too long, e.g., a taxi trip between pick-up and drop-off)
* **trips** (The sequence of all triplegs between two consecutive activity staypoints)
* **tours** (A collection of sequential trips that return to the same location)

An example plot showing the hierarchy of the *trackintel* data model can be found below:

<p align="center">
  <img width="493" height="480" src="https://github.com/mie-lab/trackintel/blob/master/docs/assets/hierarchy.png?raw=true">
</p>

The image below explicitly shows the definition of **locations** as clustered **staypoints**, generated by one or several users.

<p align="center">
  <img width="638" height="331" src="https://github.com/mie-lab/trackintel/blob/master/docs/assets/locations_with_pfs.png?raw=true">
</p>

You can enter the *trackintel* framework if your data corresponds to any of the above mentioned movement data representation. Here are some of the functionalities that we provide: 

* **Import**: Import from the following data formats is supported: `geopandas dataframes` (recommended), `csv files` in a specified format, `postGIS` databases. We also provide specific dataset readers for popular public datasets (e.g, geolife).
* **Aggregation**: We provide functionalities to aggregate into the next level of our data model. E.g., positionfixes->staypoints; positionfixes->triplegs; staypoints->locations; staypoints+triplegs->trips; trips->tours
* **Enrichment**: Activity semantics for staypoints; Mode of transport semantics for triplegs; High level semantics for locations

## How it works
*trackintel* provides support for the full life-cycle of human mobility data analysis.

**[1.]** Import data. 
```python
import geopandas as gpd
import trackintel as ti

# read pfs from csv file
pfs = ti.io.file.read_positionfixes_csv(".\examples\data\pfs.csv", sep=";", index_col="id")
# or with predefined dataset readers (here geolife) 
pfs, _ = ti.io.dataset_reader.read_geolife(".\tests\data\geolife_long")
```

**[2.]** Data model generation. 
```python
# generate staypoints and triplegs
pfs, sp = pfs.as_positionfixes.generate_staypoints(method='sliding')
pfs, tpls = pfs.as_positionfixes.generate_triplegs(sp, method='between_staypoints')
```

**[3.]** Visualization.
 ```python
# plot the generated tripleg result
ti.plot(positionfixes=pfs, staypoints=sp, triplegs=tpls, radius_sp=10)
```

**[4.]** Analysis.
 ```python
# e.g., predict travel mode labels based on travel speed
tpls = tpls.as_triplegs.predict_transport_mode()
# or calculate the temporal tracking coverage of users
tracking_coverage = ti.temporal_tracking_quality(tpls, granularity='all')
```

**[5.]** Save results.
 ```python
# save the generated results as csv file 
sp.as_staypoints.to_csv('.\examples\data\sp.csv')
tpls.as_triplegs.to_csv('.\examples\data\tpls.csv')
```

For example, the plot below shows the generated staypoints and triplegs from the imported raw positionfix data.
<p align="center">
  <img width="595" height="500" src="https://github.com/mie-lab/trackintel/blob/master/docs/_static/example_triplegs.png?raw=true">
</p>

## Installation and Usage
*trackintel* is on [pypi.org](https://pypi.org/project/trackintel/) and [conda-forge](https://anaconda.org/conda-forge/trackintel). We recommend installing trackintel via conda-forge:
```{python}
conda install -c conda-forge trackintel
```

Alternatively, you can install it with pip in a `GeoPandas` available environment using: 
```{python}
pip install trackintel
```

You should then be able to run the examples in the `examples` folder or import trackintel using:
```{python}
import trackintel as ti

ti.print_version() 
```

## Requirements and dependencies

* Numpy
* GeoPandas
* Matplotlib 
* Pint
* NetworkX
* GeoAlchemy2
* scikit-learn
* tqdm
* OSMnx
* similaritymeasures

## Development
You can find the development roadmap under `ROADMAP.md` and further development guidelines under `CONTRIBUTING.md`.

## Contributors

*trackintel* is primarily maintained by the Mobility Information Engineering Lab at ETH Zurich ([mie-lab.ethz.ch](http://mie-lab.ethz.ch)).
If you want to contribute, send a pull request and put yourself in the `AUTHORS.md` file.

## <span id="citelink">Citation</span>

If you find this code useful for your work or use it in your project, please consider citing:
```
@article{Martin_2023_trackintel,
  doi = {10.1016/j.compenvurbsys.2023.101938},
  volume = {101},
  pages = {101938},
  author = {Henry Martin and Ye Hong and Nina Wiedemann and Dominik Bucher and Martin Raubal},
  keywords = {Human mobility analysis, Open-source software, Transport planning, Data mining, Python, Tracking studies},
  title = {Trackintel: An open-source Python library for human mobility analysis},
  journal = {Computers, Environment and Urban Systems},
  year = {2023},
}
```

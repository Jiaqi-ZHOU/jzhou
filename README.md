# jzhou
J Zhou's python script to plot QE, EPW, and Wannier90 results. 

## Installation


git clone https://github.com/Jiaqi-ZHOU/jzhou.git

cd jzhou

pip install -e .

## Features

- Plot QE bands with xml file given by bands.x. 

  ```jzhou plotxmlbands example/eig/qe/aiida.xml```

- Plot QE phonon dispersion with freq file given by matdyn.x. 

  ```jzhou plotfreqbands example/ph/qe/aiida.freq -m example/ph/qe/matdyn.in```
- Plot EPW phonon dispersion with phband.freq given by epw.x.

  ```jzhou plotfreqbands example/ph/epw/phband.freq```

- Compare two bands by two xml files.

  ```jzhou plottwoxmlbands example/eig/qe/aiida.xml Label1 example/eig/qe/aiida.xml Label2```

- Compare QE bands and Wannier bands with xml and dat files. 

  ```jzhou plotxmlwanbands example/eig/qe/aiida.xml   example/eig/wannier90/aiida_band.dat```

- Plot VASP bands with several files (see --help).

  ```jzhou plotvaspbands /home/jiaqi/git/jzhou/example/eig/vasp/```
- Plot spin Hall conductivity of 2D materials, files are produced by postw90.x.

  ```jzhou plotshc  example/shc/metal/aiida-shc-fermiscan.dat  example/shc/metal/aiida.win```

- Compare VASP, Wannier90, and WannierTools bands.

  ```jzhou plotvaspwanbands example/eig/vasp/  example/eig/wannier90/wannier90_band_vasp.dat --wanfile2 example/eig/WannierTools/bulkek.dat```
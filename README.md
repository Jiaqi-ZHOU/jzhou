# jzhou
J Zhou's python script to plot QE, EPW, and Wannier90 results. 

## Installation

```bash
git clone https://github.com/Jiaqi-ZHOU/jzhou.git
cd jzhou
pip install -e .
```

## Features

- Plot QE bands with xml file given by bands.x. 

  ```bash
  jzhou plotxmlbands example/eig/qe/aiida.xml
  ```

- Plot QE phonon dispersion with freq file given by matdyn.x. 

  ```bash
  jzhou plotfreqbands example/ph/qe/aiida.freq -m example/ph/qe/matdyn.in
  ```
- Plot EPW phonon dispersion with phband.freq given by epw.x.

  ```bash
  jzhou plotfreqbands example/ph/epw/phband.freq
  ```

- Compare two bands given by two xml files.

  ```bash
  jzhou plottwoxmlbands example/eig/qe/aiida.xml Label1 example/eig/qe/aiida.xml Label2
  ```

- Compare QE bands and Wannier bands with xml and dat files. 

  ```bash
  jzhou plotxmlwanbands example/eig/qe/aiida.xml example/eig/wannier90/aiida_band.dat
  ```

- Plot VASP bands with several files (see details by --help).

  ```bash
  jzhou plotvaspbands /home/jiaqi/git/jzhou/example/eig/vasp/
  ```

- Compare VASP, Wannier90, and WannierTools bands.

  ```bash
  jzhou plotvaspwanbands example/eig/vasp/ example/eig/wannier90/wannier90_band_vasp.dat --wanfile2 example/eig/WannierTools/bulkek.dat
  ```

- Plot spin Hall conductivity of 2D material, files are produced by postw90.x.

  ```bash
  jzhou plotshc example/shc/metal/aiida-shc-fermiscan.dat example/shc/metal/aiida.win
  jzhou plotshc example/shc/insulator/aiida-shc-fermiscan.dat example/shc/insulator/aiida.win
  ```

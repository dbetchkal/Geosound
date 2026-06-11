# Geosound
A collection of `Jupyter` notebooks and Python scripts spanning a variety of practical acoustics and geography tasks.

## Environment
These notebooks use both standard Python packages and compiled C++ binaries. To manage these dependencies together, we use Conda.

Create a conda environment with the required packages from `geosound.yml` with the following command:

```shell
conda env create -f geosound.yml
```

Then, start using the environment with:

```shell
conda activate geosound
```


## Scripts

### Summarize ADS-B Data (`adsb_stats.py`)
This script recursively scans a root directory to analyze and summarize ADS-B data structured in `<YEAR> ADS-B <SITE>` folders. Because it only uses standard library modules, you don't need to install any dependencies or run from a particular environment.

Basic Usage:
```shell
python adsb_file_stats.py 'C:\\Path\\To\\Data'
```

Additional Usage Example:
Target a different file extension (e.g., .csv) and output results to a .txt:
```shell
python adsb_file_stats.py 'C:\\Path\\To\\Data' --extension .csv > adsb_file_stats_output.txt
```


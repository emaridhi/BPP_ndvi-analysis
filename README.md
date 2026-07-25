# Normal Difference Vegetation Index (NDVI) Analysis Tool
A Python tool for computing the NDVI from red and near-infrared (NIR) imagery to assess vegetation health and to
validate the complete NDVI processing pipeline. 
It was developed as the analysis companion to a multispectral imaging payload design under the Balloon Payload Program (BPP)


The project includes:
* Computing NDVI from Red and NIR band imagery
* Generating a synthetic vegetation field for testing
* Classifying vegetation health (bare, stressed, moderate, healthy)
* Visualizing results as a false-color NDVI map
* Visualizing the NDVI distribution as a histogram

## Requirements:
* Python 3.8+
* numpy
* matplotlib
* Pillow

Install dependencies <br>
`pip install numpy matplotlib pillow`

## How to Run:
1. Run in synthetic mode: Generates a simulated Red/NIR vegetation field and computes NDVI on it <br>
`python main.py`
2. Run with custom synthetic parameters: Adjusts field size, stress level, and random seed <br>
`python main.py --stress 0.6 --size 256 --seed 42`
3. Run on real imagery: Computes NDVI from your own Red-band and NIR-band grayscale images <br>
`python main.py --red red_band.png --nir nir_band.png`

## Expected Results:
* NDVI Map: A false-color heatmap where brown areas indicate stressed/sparse vegetation, yellow indicates moderate vegetation,
* and green indicates dense, healthy vegetation.
* Histogram: A continuous spread of NDVI values across the field rather than sharp spikes at one value.
* Console Summary: Mean/min/max NDVI plus a percentage breakdown of the field across four health classes.

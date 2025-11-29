# Hazelbean Tutorial Analysis Report

**Analysis Date:** 2025-11-29 14:13:14
**Project:** hazelbean_tutorial

## Summary

This analysis demonstrates the complete Hazelbean workflow from project setup through result export.

## Data Processing Steps

1. **Project Setup**: Initialized ProjectFlow with organized directories
2. **Data Loading**: Used get_path() for intelligent file discovery
3. **Processing**: Applied transformations and mathematical operations
4. **Analysis**: Performed spatial analysis and multi-raster operations
5. **Export**: Organized and documented results

## Results Summary

- **Results Array**: (50, 50) pixels
- **Value Range**: 0.04 to 99.99
- **Mean Value**: 50.32
- **Standard Deviation**: 29.37

## Classification Results

- **Class 1**: 934 pixels (37.4%)
- **Class 2**: 1022 pixels (40.9%)
- **Class 3**: 544 pixels (21.8%)

## Files Generated

- `rasters/analysis_results.npy` - Main analysis results
- `rasters/classification.npy` - Classification map
- `rasters/metadata.txt` - Raster metadata
- `reports/tutorial_analysis_report.md` - This report

## Project Structure

```
hazelbean_tutorial/
├── inputs/           # Input data
├── intermediate/     # Processing files
└── outputs/          # Final results
    └── tutorial_analysis_20251129_1413/
        ├── rasters/  # Geospatial outputs
        └── reports/  # Documentation
```

## Next Steps

- Modify parameters for your own analysis
- Use real geospatial data with coordinate systems
- Integrate with other Hazelbean functions
- Add visualization and plotting

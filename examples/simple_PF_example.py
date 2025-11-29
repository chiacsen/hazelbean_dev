"""
Complete ProjectFlow Example with Proper Geospatial Export
Demonstrates the full workflow including saving results as proper GeoTIFFs
"""

import hazelbean as hb
import numpy as np
import os

# ============================================================================
# STEP 1: Initialize ProjectFlow
# ============================================================================

p = hb.ProjectFlow('temperature_analysis')
print(f"Project initialized at: {p.project_dir}\n")


# ============================================================================
# STEP 2: Define Task Functions
# ============================================================================

def load_base_raster(p):
    """Task 1: Load a base raster to get geospatial metadata"""
    
    p.base_raster_path = p.get_path('pyramids/ha_per_cell_900sec.tif')
    
    if p.run_this:
        print("Loading base raster for geospatial template...")
        
        # Get the geospatial metadata
        p.base_info = hb.get_raster_info_hb(p.base_raster_path)
        
        print(f"  ✓ Base raster size: {p.base_info['raster_size']}")
        print(f"  ✓ Pixel size: {p.base_info['pixel_size']}")
        print(f"  ✓ Projection: {p.base_info['projection'][:50]}...\n")
    
    return p


def create_temperature_data(p):
    """Task 2: Generate synthetic temperature data matching base raster"""
    
    p.temp_data_path = os.path.join(p.intermediate_dir, 'temperature_data.tif')
    
    if p.run_this:
        print("Creating temperature data...")
        
        # Create temperature data matching base raster dimensions
        rows, cols = p.base_info['raster_size'][1], p.base_info['raster_size'][0]
        p.temperature = 20 + 10 * np.random.randn(rows, cols)
        
        # Save as proper GeoTIFF with spatial reference
        os.makedirs(p.intermediate_dir, exist_ok=True)
        
        hb.save_array_as_geotiff(
            p.temperature,
            p.temp_data_path,
            p.base_raster_path,  # Use this as template for geospatial info
            data_type=6,  # Float32
            ndv=-9999
        )
        
        print(f"  ✓ Saved as GeoTIFF: {os.path.basename(p.temp_data_path)}")
        print(f"  Temperature range: {np.nanmin(p.temperature):.1f} to {np.nanmax(p.temperature):.1f}°C\n")
    else:
        # Load existing raster
        p.temperature = hb.as_array(p.temp_data_path)
        print(f"  ↻ Loaded existing temperature data\n")
    
    return p


def identify_heat_zones(p):
    """Task 3: Classify temperatures into zones and save as GeoTIFF"""
    
    p.zones_path = os.path.join(p.intermediate_dir, 'heat_zones.tif')
    
    if p.run_this:
        print("Classifying heat zones...")
        
        # Classify into 3 zones
        p.zones = np.zeros_like(p.temperature, dtype=np.int16)
        p.zones[p.temperature < 15] = 1  # Cold
        p.zones[(p.temperature >= 15) & (p.temperature < 25)] = 2  # Moderate  
        p.zones[p.temperature >= 25] = 3  # Hot
        
        # Save as GeoTIFF
        os.makedirs(p.intermediate_dir, exist_ok=True)
        
        hb.save_array_as_geotiff(
            p.zones,
            p.zones_path,
            p.base_raster_path,  # Template for geospatial info
            data_type=3,  # Int16
            ndv=0
        )
        
        # Count pixels in each zone
        for zone_id, zone_name in [(1, 'Cold'), (2, 'Moderate'), (3, 'Hot')]:
            count = np.sum(p.zones == zone_id)
            percent = (count / p.zones.size) * 100
            print(f"  {zone_name}: {count} pixels ({percent:.1f}%)")
        
        print(f"  ✓ Saved as GeoTIFF: {os.path.basename(p.zones_path)}\n")
    else:
        p.zones = hb.as_array(p.zones_path)
        print(f"  ↻ Loaded existing zones\n")
    
    return p


def calculate_statistics(p):
    """Task 4: Calculate statistics and export final results"""
    
    # Output paths
    p.stats_path = os.path.join(p.output_dir, 'statistics.txt')
    p.mean_by_zone_path = os.path.join(p.output_dir, 'mean_temp_by_zone.tif')
    
    if p.run_this:
        print("Calculating statistics and creating final outputs...")
        
        os.makedirs(p.output_dir, exist_ok=True)
        
        # Calculate mean temperature for each zone
        mean_by_zone = np.zeros_like(p.temperature)
        
        for zone_id in [1, 2, 3]:
            zone_mask = p.zones == zone_id
            if np.any(zone_mask):
                zone_mean = np.mean(p.temperature[zone_mask])
                mean_by_zone[zone_mask] = zone_mean
        
        # Save as GeoTIFF
        hb.save_array_as_geotiff(
            mean_by_zone,
            p.mean_by_zone_path,
            p.base_raster_path,
            data_type=6,  # Float32
            ndv=-9999
        )
        
        # Write statistics report
        with open(p.stats_path, 'w') as f:
            f.write("Temperature Analysis Statistics\n")
            f.write("=" * 60 + "\n\n")
            
            # Overall statistics
            f.write(f"Overall Mean: {np.nanmean(p.temperature):.2f}°C\n")
            f.write(f"Overall Std Dev: {np.nanstd(p.temperature):.2f}°C\n\n")
            
            # Zone statistics
            f.write("Zone-Based Analysis:\n")
            f.write("-" * 60 + "\n")
            for zone_id, zone_name in [(1, 'Cold'), (2, 'Moderate'), (3, 'Hot')]:
                zone_temps = p.temperature[p.zones == zone_id]
                if len(zone_temps) > 0:
                    f.write(f"\n{zone_name} Zone (Class {zone_id}):\n")
                    f.write(f"  Mean: {zone_temps.mean():.2f}°C\n")
                    f.write(f"  Min: {zone_temps.min():.2f}°C\n")
                    f.write(f"  Max: {zone_temps.max():.2f}°C\n")
                    f.write(f"  Std Dev: {zone_temps.std():.2f}°C\n")
                    f.write(f"  Pixel Count: {len(zone_temps):,}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("\nOutput Files:\n")
            f.write(f"- Temperature raster: {os.path.basename(p.temp_data_path)}\n")
            f.write(f"- Zone classification: {os.path.basename(p.zones_path)}\n")
            f.write(f"- Mean temp by zone: {os.path.basename(p.mean_by_zone_path)}\n")
            f.write(f"- This report: {os.path.basename(p.stats_path)}\n")
        
        print(f"  ✓ Statistics saved: {os.path.basename(p.stats_path)}")
        print(f"  ✓ Mean by zone raster saved: {os.path.basename(p.mean_by_zone_path)}\n")
    else:
        print(f"  ↻ Statistics already exist\n")
    
    return p


# ============================================================================
# STEP 3: Build Task Tree
# ============================================================================

print("=" * 60)
print("BUILDING TASK TREE")
print("=" * 60 + "\n")

p.base_task = p.add_task(load_base_raster)
p.temp_task = p.add_task(create_temperature_data)
p.zones_task = p.add_task(identify_heat_zones)
p.stats_task = p.add_task(calculate_statistics)


# ============================================================================
# STEP 4: Execute Tasks
# ============================================================================

print("=" * 60)
print("EXECUTING TASKS")
print("=" * 60 + "\n")

p.execute()


# ============================================================================
# STEP 5: Summary
# ============================================================================

print("=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
print(f"\n📁 Results location: {p.output_dir}")
print(f"📊 Statistics report: {p.stats_path}")
print(f"🗺️  GeoTIFF outputs:")
print(f"   - {p.temp_data_path}")
print(f"   - {p.zones_path}")
print(f"   - {p.mean_by_zone_path}")
print("\nYou can open the .tif files in QGIS or ArcGIS!\n")
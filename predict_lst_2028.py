import os
import argparse
import numpy as np
import rasterio
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

def build_mask(*arrays):
    valid = np.ones(arrays[0].shape, dtype=bool)
    for arr in arrays:
        valid &= ~np.isnan(arr)
        valid &= (arr > -9999)
    return valid

def run_pipeline(data_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    lst_2024_path = os.path.join(data_dir, 'lstCBE24.tif')
    lulc_2024_path = os.path.join(data_dir, 'LULC_2024_sentinel_noclouds_same_extent.tiff.tif')
    ndvi_2024_path = os.path.join(data_dir, 'ndvi_2024.tif')
    dem_path = os.path.join(data_dir, 'dem_30m.tif')
    lulc_2028_path = os.path.join(data_dir, 'lulc_2028_simulation.tif')
    ndvi_2028_path = os.path.join(data_dir, 'ndvi_2028_dynamic.tif')
    out_pred_path = os.path.join(output_dir, 'LST_2028_dynamic_predicted.tif')

    print('[1/5] Loading 2024 training rasters...')
    with rasterio.open(lst_2024_path) as src_lst:
        meta = src_lst.meta.copy()
        lst_2024 = src_lst.read(1)
    with rasterio.open(lulc_2024_path) as src:
        lulc_2024 = src.read(1)
    with rasterio.open(ndvi_2024_path) as src:
        ndvi_2024 = src.read(1)
    with rasterio.open(dem_path) as src:
        dem = src.read(1)

    valid_train = build_mask(lst_2024, lulc_2024, ndvi_2024, dem)
    valid_train &= (lst_2024 > 15.0) & (lst_2024 < 55.0)

    X_train_full = np.column_stack([lulc_2024[valid_train], ndvi_2024[valid_train], dem[valid_train]])
    y_train_full = lst_2024[valid_train]

    X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=0.20, random_state=42)

    print('[2/5] Training Random Forest Regressor...')
    rf = RandomForestRegressor(n_estimators=100, max_depth=18, min_samples_split=10, min_samples_leaf=4, n_jobs=-1, random_state=42)
    rf.fit(X_train, y_train)

    y_pred_val = rf.predict(X_val)
    r2 = r2_score(y_val, y_pred_val)
    rmse = np.sqrt(mean_squared_error(y_val, y_pred_val))
    print(f'[3/5] Validation: R2 = {r2:.3f} | RMSE = {rmse:.2f} C')

    print('[4/5] Predicting 2028 LST...')
    with rasterio.open(lulc_2028_path) as src:
        lulc_2028 = src.read(1)
    with rasterio.open(ndvi_2028_path) as src:
        ndvi_2028 = src.read(1)

    valid_pred = build_mask(lulc_2028, ndvi_2028, dem)
    X_pred = np.column_stack([lulc_2028[valid_pred], ndvi_2028[valid_pred], dem[valid_pred]])
    lst_2028_flat = rf.predict(X_pred)

    lst_2028_raster = np.full(lst_2024.shape, np.nan, dtype=np.float32)
    lst_2028_raster[valid_pred] = lst_2028_flat

    print(f'[5/5] Exporting raster to {out_pred_path}')
    meta.update(dtype=rasterio.float32, nodata=np.nan)
    with rasterio.open(out_pred_path, 'w', **meta) as dst:
        dst.write(lst_2028_raster, 1)
    print('Complete.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='./data/raw')
    parser.add_argument('--output_dir', type=str, default='./data')
    args = parser.parse_args()
    run_pipeline(args.data_dir, args.output_dir)

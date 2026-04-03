# PL/SQL Exponential Smoothing

This repository provides a PL/SQL procedure for calculating simple exponential smoothing directly within an Oracle Database. It is designed for time-series forecasting and trend analysis, applying diminishing weights to older observations.

## Overview

The procedure `EXPONENTIAL_SMOOTHING` processes sequential data and computes a smoothed forecast using the standard exponential smoothing formula. It calculates the necessary observation windows and iteratively populates a target table with the smoothed values.

## Prerequisites

* **Oracle Database:** The script is written in Oracle PL/SQL.
* **Source Data Table:** A table containing the time-series data.  
* **Target Table:** A table to store the smoothed output variables.

## Configuration

Before deploying the procedure, you may need to adjust the following variables within the script to fit your specific dataset:

* `alpha`: The smoothing factor (default is `0.2`). A higher alpha discounts older observations faster. **Note:** Ensure this is defined as `NUMBER` to prevent decimal truncation.
*  script orders data sequentially by a column named `DATUM`. Ensure your source table uses this naming convention or update the script accordingly.

# Exponential Smoothing Formula

The PL/SQL script implements the **expanded (or iterative) form** of Simple Exponential Smoothing (SES). Instead of computing the forecast recursively row-by-row ($S_t = \alpha Y_t + (1-\alpha)S_{t-1}$), the script calculates it using a set-based approach over a specific window of data.

## The Formula

Expressed mathematically, the formula used in your script is:

$$S = \sum_{k} \left[ \alpha (1-\alpha)^k \cdot Y_k \right] + (1-\alpha)^{n+1} \cdot Y_{base}$$

Where:
* **$S$**: The resulting smoothed value (forecast).
* **$\alpha$** (`alpha`): The smoothing parameter (set to 0.2 in the script). It dictates how much weight is given to recent versus older observations.
* **$Y_k$** (`KUENDIGER`): The actual historical observation at a specific time index $k$.
* **$k$** (`K`): The time index or age of the observation relative to the current calculation window.
* **$n$** (`ANZ`): The total number of observations in the current sliding window.
* **$Y_{base}$**: The oldest actual value in the specified time window, acting as the initial anchor or $S_0$

## Usage

1. Compile the procedure in your Oracle database:
   ```sql
   @EXPONENTIAL_SMOOTHING.pls

2. Execute the procedure
   ```sql
   BEGIN EXPONENTIAL_SMOOTHING; END;/


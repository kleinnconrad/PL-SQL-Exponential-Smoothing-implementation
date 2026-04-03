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

## Usage

1. Compile the procedure in your Oracle database:
   ```sql
   @EXPONENTIAL_SMOOTHING.pls

2. Execute the procedure
   ```sql
   BEGIN EXPONENTIAL_SMOOTHING; END;/


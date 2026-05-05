[![1 - Deploy Data Model (Flyway)](https://github.com/<USERNAME>/<REPO>/actions/workflows/1-flyway-deploy.yml/badge.svg)](https://github.com/<USERNAME>/<REPO>/actions/workflows/1-flyway-deploy.yml)
[![2 - Deploy PL/pgSQL Procedure](https://github.com/<USERNAME>/<REPO>/actions/workflows/2-plpgsql-deploy.yml/badge.svg)](https://github.com/<USERNAME>/<REPO>/actions/workflows/2-plpgsql-deploy.yml)

## Table of Contents

* [PL/pgSQL Exponential Smoothing](#plpgsql-exponential-smoothing)
  * [Overview](#overview)
  * [Prerequisites](#prerequisites)
  * [Configuration](#configuration)
* [Database Infrastructure & CI/CD](#database-infrastructure--cicd)
  * [Why PostgreSQL (Supabase) instead of Oracle?](#why-postgresql-supabase-instead-of-oracle)
  * [The IPv6 GitHub Actions Issue & Solution](#the-ipv6-github-actions-issue--solution)
  * [Database Migrations with Flyway](#database-migrations-with-flyway)
  * [GitHub Actions Pipelines](#github-actions-pipelines)
  * [Required GitHub Secrets](#required-github-secrets)
* [Exponential Smoothing Formula](#exponential-smoothing-formula)
  * [The Formula](#the-formula)
  * [Usage](#usage)


# PL/pgSQL Exponential Smoothing

This repository provides a handmade PL/pgSQL procedure for calculating simple exponential smoothing directly within a PostgreSQL Database (hosted on Supabase). It is designed for time-series forecasting and trend analysis, applying exponentially diminishing or growing weights to older observations.

## Overview

The procedure `exponential_smoothing` processes sequential data and computes a smoothed forecast using the standard exponential smoothing formula. It calculates the necessary observation windows and iteratively populates a target table with the smoothed values.

## Prerequisites

* **PostgreSQL Database:** The script is written in PostgreSQL's native procedural language (PL/pgSQL).
* **Source Data Table:** A table containing the time-series data.  
* **Target Table:** A table to store the smoothed output variables.

## Configuration

Before deploying the procedure, you may need to adjust the following variables within the script to fit your specific dataset:

* `alpha`: The smoothing factor (default is `0.2`). A higher alpha discounts older observations faster. **Note:** Ensure this is defined as `NUMERIC` to prevent decimal truncation.
* The script orders data sequentially by a column named `DATUM`. Ensure your source table uses this naming convention or update the script accordingly.


# Database Infrastructure & CI/CD

This project uses an automated Infrastructure-as-Code (IaC) and Continuous Integration/Continuous Deployment (CI/CD) approach using GitHub Actions to manage the database schema and procedural logic.

## Why PostgreSQL (Supabase) instead of Oracle?

Initially, this project targeted the Oracle Cloud Always Free tier. However, due to notoriously strict and opaque automated account creation blocks on Oracle Cloud Infrastructure (OCI), securing a stable, permanent free database for CI/CD became unfeasible. 

**Supabase**, a fully managed open-source alternative built on top of **PostgreSQL**, was chosen as the replacement. PostgreSQL features its own procedural language (**PL/pgSQL**) that was explicitly designed to mirror the syntax, structure, and capabilities of Oracle's PL/SQL. This allowed for an almost 1:1 translation of the mathematical logic while gaining a modern, developer-friendly cloud environment.

## The IPv6 GitHub Actions Issue & Solution

**The Problem:** Supabase provisions direct database connections using **IPv6** addresses. However, GitHub Actions virtual machines (`ubuntu-latest`) and standard Docker containers currently only support **IPv4** routing. This mismatch causes a `Network is unreachable` error when the pipeline attempts to connect to the database.

**The Solution:** To bridge this gap, we use the **Supabase Connection Pooler (Supavisor)** operating on port `6543`. 
1. The pooler provides an IPv4-compatible endpoint.
2. Because the pooler manages thousands of databases, the database username must be updated from `postgres` to include the specific tenant identifier (e.g., `postgres.[project-id]`).
3. The connection mode must be set to `Session` rather than `Transaction` to support DDL execution in Flyway.

## Database Migrations with Flyway

**Flyway** is used to manage the structural data model (tables, schemas, and static seed data). 
* Migration scripts are located in the `sql/` directory and follow a strict naming convention (e.g., `V1__Initialize_analytics_schema.sql`, `V2__Insert_more_dummy_data.sql`).
* When Flyway runs, it checks an internal state table (`flyway_schema_history`) in the Supabase database. It compares the checksums of the files in the repository against what has already been executed, ensuring that new tables and data inserts are only applied once.
* Once a file is deployed via Flyway, it becomes immutable and should not be edited. Future structural changes require a new `V` script.

## GitHub Actions Pipelines

The CI/CD flow is intentionally split into two distinct pipelines to separate structural data model changes from procedural logic updates.

1. **Deploy Data Model (Flyway)** (`1-flyway-deploy.yml`)
   * **Trigger:** Manual (`workflow_dispatch`).
   * **Action:** Pulls the official Flyway Docker image, connects to Supabase via the IPv4 JDBC pooler URL, and applies any pending versioned SQL migrations from the `sql/` folder.
   * **Use Case:** Creating new tables, modifying schemas, or bulk inserting dummy historical data.

2. **Deploy PL/pgSQL Procedure** (`2-plpgsql-deploy.yml`)
   * **Trigger:** Automatic on `push` to the `main` branch, **only** if `src/exponential_smoothing_pg.pls` is modified.
   * **Action:** Installs the native PostgreSQL client (`psql`) on the GitHub runner and executes the `.pls` file to compile the logic directly into the `analytics` schema.
   * **Use Case:** Updating math formulas, fixing bugs in the procedure, or altering the smoothing window.

## Required GitHub Secrets

To run the pipelines successfully, the following secrets must be configured in **Settings > Secrets and variables > Actions**:

* `SUPABASE_DB_USER`: Your tenant-identified username (e.g., `postgres.mtwbpvtsrpfknoyhuvks`).
* `SUPABASE_DB_PASSWORD`: Your Supabase database password.
* `SUPABASE_JDBC_URL`: The Flyway connection string using the IPv4 pooler port (e.g., `jdbc:postgresql://aws-0-eu-west-1.pooler.supabase.com:6543/postgres`).
* `SUPABASE_PSQL_URL`: The standard connection URI for the `psql` client (e.g., `postgresql://postgres.[project-id]:[password]@aws-0-eu-west-1.pooler.supabase.com:6543/postgres`).


# Exponential Smoothing Formula

The PL/pgSQL script implements the **expanded (or iterative) form** of Simple Exponential Smoothing (SES). Instead of computing the forecast recursively row-by-row ($S_t = \alpha Y_t + (1-\alpha)S_{t-1}$), the script calculates it using a set-based approach over a specific window of data.

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

1. The procedure is automatically compiled into the `analytics` schema via GitHub Actions.
2. To execute the calculation and generate the smoothed data window, run the following command in the Supabase SQL Editor:
   ```sql
   CALL analytics.exponential_smoothing();

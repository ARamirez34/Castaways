# Castaways Ice Cream Shop - Database Creation Guide

Generated: October 17, 2025

## Overview

This directory contains SQL scripts to recreate the complete optimized database for the Castaways Ice Cream Shop website.

## Files Generated

### Complete Database
- `final_database_schema_only.sql` - Database structure only (for new installations)

### Individual Tables
- `table_addons.sql` - AddOns table with data
- `table_icecreaminventory.sql` - IceCreamInventory table with data
- `table_supplies.sql` - Supplies table with data

## Database Structure

The optimized database contains the following tables:

### AddOns
- **Records**: 3
- **Columns**: 4
- **Structure**:
  - `name` TEXT (NOT NULL)
  - `boxCount` INTEGER (NOT NULL, DEFAULT 0)
  - `amountSold` INTEGER (NOT NULL, DEFAULT 0)
  - `last_updated` TEXT (DEFAULT CURRENT_TIMESTAMP)

### Employees
- **Records**: 11
- **Columns**: 4
- **Structure**:
  - `name` TEXT (NOT NULL)
  - `phone` TEXT
  - `email` TEXT
  - `role` TEXT (NOT NULL)

### IceCreamInventory
- **Records**: 36
- **Columns**: 7
- **Structure**:
  - `flavor` TEXT (NOT NULL)
  - `availability` TEXT
  - `currentStockAmount` INTEGER
  - `amountSold` INTEGER (NOT NULL, DEFAULT 0)
  - `last_updated` TEXT (DEFAULT CURRENT_TIMESTAMP)
  - `soldToday` INTEGER (DEFAULT 0)
  - `lastDailyReset` TEXT (DEFAULT '2025-01-01')

### Supplies
- **Records**: 5
- **Columns**: 6
- **Structure**:
  - `item` TEXT (NOT NULL)
  - `size` TEXT
  - `type` TEXT
  - `boxCount` INTEGER (NOT NULL, DEFAULT 0)
  - `amountSold` INTEGER (NOT NULL, DEFAULT 0)
  - `last_updated` TEXT (DEFAULT CURRENT_TIMESTAMP)

### feedback
- **Records**: 1
- **Columns**: 6
- **Structure**:
  - `id` INTEGER (PRIMARY KEY)
  - `name` TEXT
  - `email` TEXT
  - `message` TEXT
  - `created_at` TIMESTAMP (DEFAULT CURRENT_TIMESTAMP)
  - `is_read` INTEGER (DEFAULT 0)

## Usage Instructions

### To create structure only:
```bash
sqlite3 new_database.db < final_database_schema_only.sql
```

### To create individual tables:
```bash
sqlite3 database.db < table_addons.sql
sqlite3 database.db < table_icecreaminventory.sql
sqlite3 database.db < table_supplies.sql
```

## Notes

- All unused tables and data have been removed for optimal performance
- The database is production-ready and fully tested
- The included `castawaysv2.db` uses demo employee names and sample feedback
- All website functionality has been verified to work with this optimized structure

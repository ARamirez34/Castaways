-- =====================================================
-- CASTAWAYS ICE CREAM SHOP - DATABASE SCHEMA ONLY
-- Generated: October 17, 2025
-- Description: Database structure without data
-- =====================================================

-- Create all tables

-- Table: AddOns
CREATE TABLE "AddOns" (
        name TEXT NOT NULL,
        boxCount INTEGER NOT NULL DEFAULT 0,
        amountSold INTEGER NOT NULL DEFAULT 0,
        last_updated TEXT DEFAULT CURRENT_TIMESTAMP
    );

-- Table: Employees
CREATE TABLE Employees (
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        role TEXT NOT NULL
    );

-- Table: IceCreamInventory
CREATE TABLE "IceCreamInventory" (
        flavor TEXT NOT NULL,
        availability TEXT,
        currentStockAmount INTEGER,
        amountSold INTEGER NOT NULL DEFAULT 0,
        last_updated TEXT DEFAULT CURRENT_TIMESTAMP
    , soldToday INTEGER DEFAULT 0, lastDailyReset TEXT DEFAULT '2025-01-01');

-- Table: Supplies
CREATE TABLE "Supplies" (
        item TEXT NOT NULL,
        size TEXT,
        type TEXT,
        boxCount INTEGER NOT NULL DEFAULT 0,
        amountSold INTEGER NOT NULL DEFAULT 0,
        last_updated TEXT DEFAULT CURRENT_TIMESTAMP
    );

-- Table: feedback
CREATE TABLE feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        , is_read INTEGER DEFAULT 0);

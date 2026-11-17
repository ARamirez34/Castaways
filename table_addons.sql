-- =====================================================
-- TABLE: AddOns
-- Generated: October 17, 2025
-- =====================================================

-- Create table
CREATE TABLE "AddOns" (
        name TEXT NOT NULL,
        boxCount INTEGER NOT NULL DEFAULT 0,
        amountSold INTEGER NOT NULL DEFAULT 0,
        last_updated TEXT DEFAULT CURRENT_TIMESTAMP
    );

-- Insert data (3 records)
INSERT INTO AddOns (name, boxCount, amountSold, last_updated) VALUES ('Cereal', 0, 1, '2025-10-07');
INSERT INTO AddOns (name, boxCount, amountSold, last_updated) VALUES ('Hot Fudge', 1, 0, '2025-10-07');
INSERT INTO AddOns (name, boxCount, amountSold, last_updated) VALUES ('Caramel', 2, 0, '2025-10-07');

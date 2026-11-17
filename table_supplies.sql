-- =====================================================
-- TABLE: Supplies
-- Generated: October 17, 2025
-- =====================================================

-- Create table
CREATE TABLE "Supplies" (
        item TEXT NOT NULL,
        size TEXT,
        type TEXT,
        boxCount INTEGER NOT NULL DEFAULT 0,
        amountSold INTEGER NOT NULL DEFAULT 0,
        last_updated TEXT DEFAULT CURRENT_TIMESTAMP
    );

-- Insert data (5 records)
INSERT INTO Supplies (item, size, type, boxCount, amountSold, last_updated) VALUES ('Cup', 'Keiki', 'Paper', 2, 0, '2025-10-01');
INSERT INTO Supplies (item, size, type, boxCount, amountSold, last_updated) VALUES ('Cup', 'Small', 'Paper', 3, 0, '2025-10-01');
INSERT INTO Supplies (item, size, type, boxCount, amountSold, last_updated) VALUES ('Cup', 'Large', 'Paper', 1, 0, '2025-10-01');
INSERT INTO Supplies (item, size, type, boxCount, amountSold, last_updated) VALUES ('Cone', '', 'Sugar', 4, 0, '2025-10-01');
INSERT INTO Supplies (item, size, type, boxCount, amountSold, last_updated) VALUES ('Bowl', 'NA', 'Plastic', 2, 1, '2025-10-07');

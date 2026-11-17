-- =====================================================
-- TABLE: IceCreamInventory
-- Generated: October 17, 2025
-- =====================================================

-- Create table
CREATE TABLE "IceCreamInventory" (
        flavor TEXT NOT NULL,
        availability TEXT,
        currentStockAmount INTEGER,
        amountSold INTEGER NOT NULL DEFAULT 0,
        last_updated TEXT DEFAULT CURRENT_TIMESTAMP
    , soldToday INTEGER DEFAULT 0, lastDailyReset TEXT DEFAULT '2025-01-01');

-- Insert data (36 records)
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Vanilla', 'Full', 10, 5, '2025-10-17', 1, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Vanilla Bean', 'Full', 8, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Coconut', 'Half', 3, 3, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Pandan w/ Coconut', 'Full', 5, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Biscoff Butter Cookies', 'Low', 1, 1, '2025-10-17', 1, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Chocolate Chip Cookies', 'Low', 1, 1, '2025-10-17', 1, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Cookies Galore', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Mango', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Strawberry', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Cherry w/ Chocolate Chip', 'Low', 1, 1, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Blackberry', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Lychee w/ mochi', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Blackberry pie', 'Empty', 0, 1, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Cotton Candy', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Birthday Cake', 'Empty', 0, 1, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Blueberry', 'Low', 1, 1, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Matcha', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Orange', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Peanut Butter', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Ube', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Ube w/ Coconut', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Cookies n Cream', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Chocolate Chip', 'Empty', 0, 2, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Vanilla w/ Chocolate Swirl', 'Half', 2, 5, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Cookie Dough', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Coffee', 'Empty', 0, 1, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Honey Vanilla', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Honey Almond', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Roasted Walnut', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Pistachio', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Chocolate w/ Brownie', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Butter Almond', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Yuzu', 'Low', 1, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Guava', 'Empty', 0, 0, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('zoozoo', 'Low', 1, 2, '2025-10-17', 0, '2025-10-17');
INSERT INTO IceCreamInventory (flavor, availability, currentStockAmount, amountSold, last_updated, soldToday, lastDailyReset) VALUES ('Li Hing Mango', 'Half', 3, 1, '2025-10-17', 0, '2025-10-17');

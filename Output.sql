-- Query for Table_OrderID
CREATE TABLE Table_OrderID AS SELECT TotalFoodCost, Date, TotalDrinkCost, TotalCost, CustomerID, OrderID, CustomerName FROM MainData;;

-- Query for Table_OrderID
CREATE TABLE Table_OrderID AS SELECT TotalFoodCost, Date, TotalDrinkCost, TotalCost, CustomerID, OrderID, CustomerName FROM MainData;;

-- Query for Table_DrinkID_OrderID
CREATE TABLE Table_DrinkID_OrderID AS SELECT DrinkQuantity, DrinkID, Milk, DrinkSize, OrderID FROM MainData;;

-- Query for Table_FoodID_OrderID
CREATE TABLE Table_FoodID_OrderID AS SELECT FoodID, FoodQuantity, OrderID FROM MainData;;

-- Query for Table_CustomerID
CREATE TABLE Table_CustomerID AS SELECT CustomerName, CustomerID FROM MainData;;

-- Query for Table_DrinkID
CREATE TABLE Table_DrinkID AS SELECT DrinkID, DrinkName FROM MainData;;

-- Query for Table_FoodID
CREATE TABLE Table_FoodID AS SELECT FoodID, FoodName FROM MainData;;

-- Query for MVD_Table_OrderID
CREATE TABLE MVD_Table_OrderID AS SELECT FoodID, DrinkID, OrderID FROM MainData;;

-- Query for 5NF_Table_OrderID
CREATE TABLE 5NF_Table_OrderID AS SELECT TotalFoodCost, Date, TotalDrinkCost, TotalCost, CustomerID, OrderID, CustomerName FROM MainData;;

-- Query for 5NF_Table_DrinkID_OrderID
CREATE TABLE 5NF_Table_DrinkID_OrderID AS SELECT DrinkQuantity, DrinkID, Milk, DrinkSize, OrderID FROM MainData;;

-- Query for 5NF_Table_FoodID_OrderID
CREATE TABLE 5NF_Table_FoodID_OrderID AS SELECT FoodID, FoodQuantity, OrderID FROM MainData;;

-- Query for 5NF_Table_CustomerID
CREATE TABLE 5NF_Table_CustomerID AS SELECT CustomerName, CustomerID FROM MainData;;

-- Query for 5NF_Table_DrinkID
CREATE TABLE 5NF_Table_DrinkID AS SELECT DrinkID, DrinkName FROM MainData;;

-- Query for 5NF_Table_FoodID
CREATE TABLE 5NF_Table_FoodID AS SELECT FoodID, FoodName FROM MainData;;


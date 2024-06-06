create database billing;
use billing;

create table Cashiers(
  cashierID varchar(50) primary key not null,
  cashierName varchar(100) not null,
  shift varchar(50) not null
);
create table items(
  itemID varchar(30) primary key not null,
  itemName varchar(50) not null,
  category enum('hot drink', 'iced drink', 'frapped drink', 'cake') not null,
  sizeOption enum('S', 'L') default null,
    price decimal(10,2) not null
);
create table Orders(
  orderID int primary key auto_increment,
  orderDate datetime default current_timestamp,
  cashierID varchar(50),
    totalAmount decimal(10,2),
    foreign key (cashierID) references Cashiers(cashierID)
);
create table Order_Items(
  orderItemID int primary key auto_increment,
  orderID int,
    itemID varchar(30),
    discount decimal(10, 2),
    quantity int not null default 1, 
    foreign key (orderID) references Orders(orderID),
    foreign key (itemID) references items(itemID)
);
DELIMITER //
DELIMITER //

CREATE PROCEDURE InsertItem (
    IN p_itemID VARCHAR(30),
    IN p_itemName VARCHAR(50),
    IN p_category ENUM('hot drink', 'iced drink', 'frapped drink', 'cake'),
    IN p_sizeOption ENUM('S', 'L'),
    IN p_price DECIMAL(10,2)
)
BEGIN
    INSERT INTO items (itemID, itemName, category, sizeOption, price)
    VALUES (p_itemID, p_itemName, p_category, p_sizeOption, p_price);
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE DeleteItem (
    IN p_itemID VARCHAR(30)
)
BEGIN
    DELETE FROM items WHERE itemID = p_itemID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE ViewOrder (
    IN p_orderID INT
)
BEGIN
    SELECT 
        o.orderID, 
        o.orderDate, 
        c.cashierName, 
        o.totalAmount,
        oi.orderItemID,
        i.itemName,
        i.category,
        i.sizeOption,
        oi.discount,
        oi.quantity,
        i.price,
        (i.price * oi.quantity) - oi.discount AS totalPrice
    FROM 
        Orders o
        JOIN Cashiers c ON o.cashierID = c.cashierID
        JOIN Order_Items oi ON o.orderID = oi.orderID
        JOIN items i ON oi.itemID = i.itemID
    WHERE 
        o.orderID = p_orderID;
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE InsertOrder (
    IN p_cashierID VARCHAR(50),
    IN p_totalAmount DECIMAL(10,2)
)
BEGIN
    INSERT INTO Orders (cashierID, totalAmount)
    VALUES (p_cashierID, p_totalAmount);
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE UpdateOrder (
    IN p_orderID INT,
    IN p_cashierID VARCHAR(50),
    IN p_totalAmount DECIMAL(10,2)
)
BEGIN
    UPDATE Orders 
    SET 
        cashierID = p_cashierID,
        totalAmount = p_totalAmount
    WHERE 
        orderID = p_orderID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE InsertOrderItem (
    IN p_orderID INT,
    IN p_itemID VARCHAR(30),
    IN p_discount DECIMAL(10, 2),
    IN p_quantity INT
)
BEGIN
    INSERT INTO Order_Items (orderID, itemID, discount, quantity)
    VALUES (p_orderID, p_itemID, p_discount, p_quantity);
END //

CREATE PROCEDURE UpdateOrderTotalAmount (
    IN p_orderID INT
)
BEGIN
    UPDATE Orders
    SET totalAmount = (
        SELECT SUM((i.price * oi.quantity) - oi.discount)
        FROM Order_Items oi
        JOIN items i ON oi.itemID = i.itemID
        WHERE oi.orderID = p_orderID
    )
    WHERE orderID = p_orderID;
END //

DELIMITER ;

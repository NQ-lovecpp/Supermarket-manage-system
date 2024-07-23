当然可以！以下是一个完整的MySQL脚本，用于创建数据库和表结构。

### 创建数据库脚本

```sql
-- 创建数据库
CREATE DATABASE `小型超市管理系统`;

-- 使用数据库
USE `小型超市管理系统`;
```

### 创建表结构脚本

#### Category 表

```sql
CREATE TABLE `Category` (
    `category_id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

#### Employee 表

```sql
CREATE TABLE `Employee` (
    `employee_id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `position` varchar(50) NULL,
    `phone` varchar(20) NULL,
    `hire_date` date NULL,
    PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

#### Product 表

```sql
CREATE TABLE `Product` (
    `product_id` int NOT NULL AUTO_INCREMENT,
    `category_id` int NULL,
    `name` varchar(50) NOT NULL,
    `price` decimal(10, 2) NOT NULL,
    `quantity` int NOT NULL,
    PRIMARY KEY (`product_id`),
    FOREIGN KEY (`category_id`) REFERENCES `Category`(`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

#### Purchase 表

```sql
CREATE TABLE `Purchase` (
    `purchase_id` int NOT NULL AUTO_INCREMENT,
    `product_id` int NULL,
    `supplier_id` int NULL,
    `quantity` int NOT NULL,
    `unit_price` decimal(10, 2) NOT NULL,
    `purchase_date` date NOT NULL,
    PRIMARY KEY (`purchase_id`),
    FOREIGN KEY (`product_id`) REFERENCES `Product`(`product_id`),
    FOREIGN KEY (`supplier_id`) REFERENCES `Supplier`(`supplier_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

#### Sale 表

```sql
CREATE TABLE `Sale` (
    `sale_id` int NOT NULL AUTO_INCREMENT,
    `product_id` int NULL,
    `quantity` int NOT NULL,
    `unit_price` decimal(10, 2) NOT NULL,
    `sale_date` date NOT NULL,
    `employee_id` int NULL,
    PRIMARY KEY (`sale_id`),
    FOREIGN KEY (`product_id`) REFERENCES `Product`(`product_id`),
    FOREIGN KEY (`employee_id`) REFERENCES `Employee`(`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

#### Supplier 表

```sql
CREATE TABLE `Supplier` (
    `supplier_id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `contact_name` varchar(50) NULL,
    `phone` varchar(20) NULL,
    PRIMARY KEY (`supplier_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

### 完整脚本

将所有上述脚本组合在一起，形成一个完整的MySQL脚本：

```sql
-- 创建数据库
CREATE DATABASE `小型超市管理系统`;

-- 使用数据库
USE `小型超市管理系统`;

-- 创建 Category 表
CREATE TABLE `Category` (
    `category_id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建 Supplier 表
CREATE TABLE `Supplier` (
    `supplier_id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `contact_name` varchar(50) NULL,
    `phone` varchar(20) NULL,
    PRIMARY KEY (`supplier_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建 Employee 表
CREATE TABLE `Employee` (
    `employee_id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `position` varchar(50) NULL,
    `phone` varchar(20) NULL,
    `hire_date` date NULL,
    PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建 Product 表
CREATE TABLE `Product` (
    `product_id` int NOT NULL AUTO_INCREMENT,
    `category_id` int NULL,
    `name` varchar(50) NOT NULL,
    `price` decimal(10, 2) NOT NULL,
    `quantity` int NOT NULL,
    PRIMARY KEY (`product_id`),
    FOREIGN KEY (`category_id`) REFERENCES `Category`(`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建 Purchase 表
CREATE TABLE `Purchase` (
    `purchase_id` int NOT NULL AUTO_INCREMENT,
    `product_id` int NULL,
    `supplier_id` int NULL,
    `quantity` int NOT NULL,
    `unit_price` decimal(10, 2) NOT NULL,
    `purchase_date` date NOT NULL,
    PRIMARY KEY (`purchase_id`),
    FOREIGN KEY (`product_id`) REFERENCES `Product`(`product_id`),
    FOREIGN KEY (`supplier_id`) REFERENCES `Supplier`(`supplier_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建 Sale 表
CREATE TABLE `Sale` (
    `sale_id` int NOT NULL AUTO_INCREMENT,
    `product_id` int NULL,
    `quantity` int NOT NULL,
    `unit_price` decimal(10, 2) NOT NULL,
    `sale_date` date NOT NULL,
    `employee_id` int NULL,
    PRIMARY KEY (`sale_id`),
    FOREIGN KEY (`product_id`) REFERENCES `Product`(`product_id`),
    FOREIGN KEY (`employee_id`) REFERENCES `Employee`(`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

```

这个脚本将创建一个名为 `小型超市管理系统` 的数据库，并在其中创建必要的表，包括外键约束。您可以将这个脚本保存为一个 `.sql` 文件，并在MySQL中运行它来创建数据库和表。

<br>

---

以下是插入测试数据的SQL脚本，每个表插入10条数据：

### 插入 `Category` 表数据

```sql
INSERT INTO `Category` (`name`) VALUES
('Beverages'),
('Condiments'),
('Confections'),
('Dairy Products'),
('Grains/Cereals'),
('Meat/Poultry'),
('Produce'),
('Seafood'),
('Snacks'),
('Frozen Foods');
```

### 插入 `Supplier` 表数据

```sql
INSERT INTO `Supplier` (`name`, `contact_name`, `phone`) VALUES
('Supplier A', 'Alice', '123-456-7890'),
('Supplier B', 'Bob', '123-456-7891'),
('Supplier C', 'Charlie', '123-456-7892'),
('Supplier D', 'David', '123-456-7893'),
('Supplier E', 'Eve', '123-456-7894'),
('Supplier F', 'Frank', '123-456-7895'),
('Supplier G', 'Grace', '123-456-7896'),
('Supplier H', 'Hank', '123-456-7897'),
('Supplier I', 'Ivy', '123-456-7898'),
('Supplier J', 'Jack', '123-456-7899');
```

### 插入 `Employee` 表数据

```sql
INSERT INTO `Employee` (`name`, `position`, `phone`, `hire_date`) VALUES
('John Doe', 'Manager', '987-654-3210', '2023-01-01'),
('Jane Smith', 'Cashier', '987-654-3211', '2023-02-01'),
('Emily Johnson', 'Stock Clerk', '987-654-3212', '2023-03-01'),
('Michael Brown', 'Salesperson', '987-654-3213', '2023-04-01'),
('Jessica Davis', 'Cleaner', '987-654-3214', '2023-05-01'),
('William Wilson', 'Security', '987-654-3215', '2023-06-01'),
('Olivia Martinez', 'Cashier', '987-654-3216', '2023-07-01'),
('James Anderson', 'Stock Clerk', '987-654-3217', '2023-08-01'),
('Sophia Thomas', 'Salesperson', '987-654-3218', '2023-09-01'),
('Benjamin Taylor', 'Manager', '987-654-3219', '2023-10-01');
```

### 插入 `Product` 表数据

```sql
INSERT INTO `Product` (`category_id`, `name`, `price`, `quantity`) VALUES
(1, 'Coca Cola', 1.00, 100),
(2, 'Ketchup', 2.00, 50),
(3, 'Chocolate', 1.50, 200),
(4, 'Milk', 1.20, 80),
(5, 'Rice', 0.80, 150),
(6, 'Chicken', 5.00, 70),
(7, 'Apple', 0.50, 120),
(8, 'Salmon', 10.00, 30),
(9, 'Chips', 1.20, 60),
(10, 'Ice Cream', 3.00, 40);
```

### 插入 `Purchase` 表数据

```sql
INSERT INTO `Purchase` (`product_id`, `supplier_id`, `quantity`, `unit_price`, `purchase_date`) VALUES
(1, 1, 50, 0.90, '2023-01-01'),
(2, 2, 30, 1.80, '2023-02-01'),
(3, 3, 100, 1.20, '2023-03-01'),
(4, 4, 40, 1.00, '2023-04-01'),
(5, 5, 60, 0.70, '2023-05-01'),
(6, 6, 20, 4.50, '2023-06-01'),
(7, 7, 70, 0.40, '2023-07-01'),
(8, 8, 15, 9.00, '2023-08-01'),
(9, 9, 35, 1.00, '2023-09-01'),
(10, 10, 25, 2.50, '2023-10-01');
```

### 插入 `Sale` 表数据

```sql
INSERT INTO `Sale` (`product_id`, `quantity`, `unit_price`, `sale_date`, `employee_id`) VALUES
(1, 5, 1.00, '2023-01-10', 1),
(2, 3, 2.00, '2023-02-10', 2),
(3, 10, 1.50, '2023-03-10', 3),
(4, 4, 1.20, '2023-04-10', 4),
(5, 8, 0.80, '2023-05-10', 5),
(6, 7, 5.00, '2023-06-10', 6),
(7, 12, 0.50, '2023-07-10', 7),
(8, 2, 10.00, '2023-08-10', 8),
(9, 6, 1.20, '2023-09-10', 9),
(10, 3, 3.00, '2023-10-10', 10);
```

将这些SQL插入语句依次执行，即可在每个表中插入10条测试数据。
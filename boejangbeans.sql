-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 19, 2024 at 07:44 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `boejangbeans`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `id` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `salt` varchar(32) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`id`, `fname`, `lname`, `username`, `email`, `password_hash`, `salt`, `created_at`) VALUES
(2, 'Rafli', 'Prasetyo', 'Rafli', 'rafly4595@gmail.com', 'scrypt:32768:8:1$JCcjGABBgmhKL8oq$89d9b56020b52c1581d2df08f801c51815f81a3da20824b7c139fdbd6aadfbdd2315bf4a52243232260df3ac7cdf2f74815f33393c2f24a151ee04f6a9b54ea3', '5d221bee176bb55974fe3be9c6b64213', '2024-12-19 17:53:17'),
(3, 'Azzam', 'Mazzed', 'Azzam', 'mazeed@gmail.com', 'scrypt:32768:8:1$6Vd5kfrMJrekj1cI$5f13a98ffa3cec8f849232ea405dfd6f0423a112c15cc724f34f174cafa48c7eb60aa9da1d8cf0e6924fc9ce123c5d51a590a5deb483a2aedf8736bd443a88c1', 'a1f7b621ded97403786bcfec9d3465b7', '2024-12-19 18:14:17'),
(4, 'Nagita', 'Zachawerus', 'Nagita', 'nagita@gmail.com', 'scrypt:32768:8:1$IpmftX7aFUhIgYUs$4e1f83c83deb76427afd350630a40e79001bcbc433e9e5dae6dc8fced91f9f82ee1587f771519f4ca386355b2e9139f497a3c02db00b187bd2975d4334c731ea', '1411dbde12593c996ba442bab7b5a308', '2024-12-19 18:14:26'),
(5, 'Faqih', 'Muttaqin', 'Faqih', 'faqih123@gmail.com', 'scrypt:32768:8:1$lDQ7rqYN1GgIQcnh$e84d057e49f6b6b327ee2b490815650ce65ac30648e907b31ba3cf793a3f748588a1de9012ebbc5a6e86dfc2ceb2568c6a011f7eb0d7a2d13e56d4f583e4d64d', '2b822ee24c43e67b3742a596f13fc6c2', '2024-12-19 18:14:38');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `email` varchar(30) NOT NULL,
  `no_hp` varchar(12) NOT NULL,
  `pesan` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`id`, `nama`, `email`, `no_hp`, `pesan`) VALUES
(1, 'Rafli Ilham Prasetyo', 'rafly4595@gmail.com', '085155043588', 'Takde cawan kah ????'),
(2, 'Sumbul Azzed Abdullah', 'mazeed@gmail.com', '080808080808', 'Gass Mabar !!!');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `harga` int(11) NOT NULL,
  `stok` int(11) NOT NULL,
  `foto` varchar(255) NOT NULL,
  `typeCoffee` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `nama`, `harga`, `stok`, `foto`, `typeCoffee`) VALUES
(1, 'Toraja Sapan 200gr', 105000, 20, '2.jpg', 'Strong'),
(2, 'Aceh Gayo Wine 200gr', 125000, 100, '2.jpg', 'Strong'),
(3, 'Aceh Gayo Honey 150gr', 94000, 80, '2.jpg', 'Low'),
(4, 'Bali Kintamani 200gr', 124000, 100, '2.jpg', 'Medium'),
(5, 'Flores Bajawa 200gr', 124000, 100, '2.jpg', 'Low'),
(6, 'Papua Paneli 200gr', 148000, 100, '2.jpg', 'Low'),
(9, 'Rafli Prasetyo', 145000, 55, '2.jpg', 'Medium');

-- --------------------------------------------------------

--
-- Table structure for table `purchases`
--

CREATE TABLE `purchases` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `payment_method` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `address` text NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `purchased_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`id`, `user_id`, `product_id`, `quantity`, `total_price`, `payment_method`, `email`, `address`, `phone_number`, `purchased_at`) VALUES
(12, 2, 5, 2, 248000.00, 'credit_card', 'rafly4595@gmail.com', 'Sleman', '085155043588', '2024-12-19 17:57:11'),
(14, 2, 6, 1, 148000.00, 'bank_transfer', 'rafly4595@gmail.com', 'Sleman', '085155043588', '2024-12-19 17:58:49'),
(15, 2, 2, 1, 125000.00, 'bank_transfer', 'rafly4595@gmail.com', 'Sleman', '085155043588', '2024-12-19 17:58:49'),
(17, 5, 5, 1, 124000.00, 'bank_transfer', 'faqih123@gmail.com', 'Bone', '080808080808', '2024-12-19 18:15:12'),
(18, 5, 6, 2, 296000.00, 'bank_transfer', 'faqih123@gmail.com', 'Bone', '080808080808', '2024-12-19 18:15:12'),
(19, 4, 4, 1, 124000.00, 'bank_transfer', 'nagita@gmail.com', 'Manado', '0867854321', '2024-12-19 18:17:47'),
(20, 4, 1, 1, 105000.00, 'bank_transfer', 'nagita@gmail.com', 'Manado', '0867854321', '2024-12-19 18:17:47'),
(21, 4, 2, 1, 125000.00, 'bank_transfer', 'nagita@gmail.com', 'Manado', '0867854321', '2024-12-19 18:17:47');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `purchases`
--
ALTER TABLE `purchases`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `purchases`
--
ALTER TABLE `purchases`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `account` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `purchases`
--
ALTER TABLE `purchases`
  ADD CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `account` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `purchases_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

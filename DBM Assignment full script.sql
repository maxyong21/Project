create database dbmAssignment;
use dbmAssignment;

create table Member 
(MemberID nvarchar(50) not null primary key,
MemberName nvarchar(50),
Role nvarchar(50),
Gender nvarchar(50),
ContactNum nvarchar(50));

insert into Member values
('APUM001', 'Gal Gadot', 'Staff', 'Female', '018-3658365'),
('APUM002', 'Benjamin Franklin', 'Staff', 'Male', '013-5846777'),
('APUM003', 'Thomas Jefferson', 'Student', 'Male', '015-14675446'),
('APUM004', 'Wang Lei', 'Staff',  'Male', '016-8468456'),
('APUM005', 'Yang Bao Bei', 'Student', 'Female', '011-4655635');


create table Food
(FoodID nvarchar(50) not null primary key,
FoodName nvarchar(50),
Price decimal(10,2),
QuantitySold int);

insert into Food values
('F01', 'Nasi Lemak', '5', '4'),
('F02', 'Roti Canai', '2', '3'),
('F03', 'Maggi Goreng', '4.5', '2'),
('F04', 'Mee Soup', '5', '2'),
('F05', 'Chicken Chop', '15', '4');


create table Feedback
(RateID nvarchar(50) not null primary key,
FoodID nvarchar(50) foreign key references Food(FoodID),
MemberID nvarchar(50) foreign key references Member(MemberID),
Rating decimal(10,2));

insert into Feedback values
('R01', 'F01', 'APUM001', '5'),
('R02', 'F04', 'APUM002', '2'),
('R03', 'F01', 'APUM002', '3'),
('R04', 'F02', 'APUM005', '5'),
('R05', 'F05', 'APUM001', '4'),
('R06', 'F01', 'APUM004', '5'),
('R07', 'F02', 'APUM001', '2'),
('R08', 'F03', 'APUM004', '5'),
('R09', 'F05', 'APUM002', '5'),
('R10', 'F02', 'APUM004', '4'),
('R11', 'F03', 'APUM005', '1'),
('R12', 'F04', 'APUM004', '3'),
('R13', 'F01', 'APUM003', '4'),
('R14', 'F05', 'APUM003', '4');


create table ShoppingCart
(CartID nvarchar(50) not null primary key,
FoodID nvarchar(50) foreign key references Food(FoodID),
MemberID nvarchar(50) foreign key references Member(MemberID),
Quantity int,
TotalCost decimal(10,2),
PaymentStatus nvarchar(50));

insert into ShoppingCart values
('C01', 'F01', 'APUM005', '1', '5', 'Paid'),
('C02', 'F02', 'APUM002', '3', '6', 'Unpaid'),
('C03', 'F03', 'APUM003', '2', '9', 'Paid'),
('C04', 'F03', 'APUM002', '1', '4.5', 'Paid'),
('C05', 'F05', 'APUM001', '1', '15', 'Paid'),
('C06', 'F03', 'APUM001', '1', '2', 'Paid'),
('C07', 'F05', 'APUM001', '2', '30', 'Unpaid'),
('C08', 'F04', 'APUM004', '5', '25', 'Paid'),
('C09', 'F04', 'APUM001', '1', '5', 'Paid');


create table Worker
(WorkerID nvarchar(50) not null primary key,
WorkerName nvarchar(50),
Position nvarchar(50),
ShiftTimeHours decimal(10,2));

insert into Worker values
('W01', 'John', 'Manager', '10'),
('W02', 'Sam', 'Chef', '5'),
('W03', 'Joan', 'Chef', '5'),
('W04', 'Betty', 'Chef', '5'),
('W05', 'Tom', 'Dispatch Worker', '7'),
('W06', 'Smith', 'Dispatch Worker', '4'),
('W07', 'Alex', 'Dispatch Worker', '7');


create table MealOrder
(OrderID nvarchar(50) not null primary key,
CartID nvarchar(50) foreign key references ShoppingCart(CartID),
MemberID nvarchar(50) foreign key references Member(MemberID),
WorkerID nvarchar(50) foreign key references Worker(WorkerID),
Date datetime);

insert into MealOrder values
('OR01', 'C01', 'APUM005', 'W02', '10 Jan 2024 13:00:00'),
('OR02', 'C03', 'APUM003', 'W02', '15 Jan 2024 10:30:00'),
('OR03', 'C04', 'APUM002', 'W04', '22 Jan 2024 14:25:00'),
('OR04', 'C05', 'APUM001', 'W03', '1 Feb 2024 17:00:00'),
('OR05', 'C06', 'APUM001', 'W04', '5 Feb 2024 9:00:00'),
('OR06', 'C08', 'APUM004', 'W03', '10 Feb 2024 10:00:00'),
('OR07', 'C09', 'APUM001', 'W02', '17 Feb 2024 13:45:00');


create table Payment
(PaymentID nvarchar(50) not null primary key,
MemberID nvarchar(50) foreign key references Member(MemberID),
CartID nvarchar(50) foreign key references ShoppingCart(CartID),
PaymentMethod nvarchar(50));

insert into Payment values
('P01', 'APUM005', 'C01', 'Cash'),
('P02', 'APUM003', 'C03', 'Cash'),
('P03', 'APUM002', 'C04', 'Cashless'),
('P04', 'APUM004', 'C05', 'Cash'),
('P05', 'APUM001', 'C06', 'Cashless'),
('P06', 'APUM004', 'C08', 'Cashless'),
('P07', 'APUM001', 'C09', 'Cash');


create table DeliveryStatus
(DeliveryID nvarchar(50) not null primary key,
OrderID nvarchar(50) foreign key references MealOrder(OrderID),
WorkerID nvarchar(50) foreign key references Worker(WorkerID),
Status nvarchar(50));

insert into DeliveryStatus values
('D01', 'OR01', 'W05', 'Delivered'),
('D02', 'OR02', 'W07', 'Not Delivered'),
('D03', 'OR03', 'W06', 'Not Delivered'),
('D04', 'OR04', 'W05', 'Delivered'),
('D05', 'OR05', 'W06', 'Delivered'),
('D06', 'OR06', 'W07', 'Delivered'),
('D07', 'OR07', 'W06', 'Delivered');



--i) List the food(s) which has the highest rating. Show food id, food name and the rating. 
select f.FoodID, f.FoodName, avg(r.Rating) as [Highest Rating] from Food f
inner join Feedback r
on f.FoodID = r.FoodID
group by f.FoodID, f.FoodName
having avg(r.Rating) like (select max(avgRating) as [HighestRating] from 
(select avg(r.Rating) as [avgRating] from Feedback r group by r.FoodID) as [HighestRating]);


--ii) Find the total number of feedback per member. Show member id, member name and total number of feedback per member. 
select r.MemberID, m.MemberName, count(r.Rating) as [Total Feedback] from Feedback r
full outer join Member m
on r.MemberID = m.MemberID
group by r.MemberID, m.MemberName;


--iii) Find the total number of food(meal) ordered by manager from each chef. 
select o.WorkerID, count(o.OrderID) as [Total Orders] from MealOrder o
group by o.WorkerID;


--iv) Find the total number of food(meal) cooked by each chef. Show chef id, chef name, and number of meals cooked. 
select o.WorkerID as [ChefID], w.WorkerName as [ChefName], count(o.OrderID) as [Total Meals Cooked] from MealOrder o
inner join Worker w
on o.WorkerID = w.WorkerID
group by o.WorkerID, w.WorkerName;


--v) List all the food where its average rating is more than the average rating of all food. 
select f.FoodID, f.FoodName, avg(r.Rating) as [Rating] from Food f
inner join Feedback r
on f.FoodID = r.FoodID
group by f.FoodID, f.FoodName 
having avg(r.Rating) >
(select avg(avgRating) as [Overall Average] from 
(select avg(r.Rating) as [avgRating] from Feedback r group by r.FoodID) 
as [Overall Average])
order by [Rating] desc;


--vi) Find the top 3 bestselling food(s). The list should include id, name, price and quantity sold. 
select top 3 * from Food
order by QuantitySold desc;


--vii) Show the top 3 members who spent most on ordering food. List should include id and name and whether they student or staff. 
select top 3 m.MemberID, m.MemberName, m.Role, sum(s.TotalCost) as [Total Spent] from Member m
inner join ShoppingCart s
on m.MemberID = s.MemberID
group by m.MemberID, m.MemberName, m.Role
order by [Total Spent] desc;


--viii) Show the total members based on gender who are registered as members. List should include id, name, role(student/staff) and gender. 
select m.MemberID, m.MemberName, m.Role, m.Gender from Member m
order by m.Gender;


--ix) Show a list of ordered food which has not been delivered to members. 
--The list should show member id, role(student/staff), contact number, food id, food name, quantity, date, and status of delivery. 
select m.MemberID, m.Role, m.ContactNum, s.FoodID, f.FoodName, s.Quantity, o.Date, d.Status from ShoppingCart s
inner join Member m on s.MemberID = m.MemberID
inner join Food f on s.FoodID = f.FoodID
inner join MealOrder o on o.MemberID = m.MemberID
inner join DeliveryStatus d on o.OrderID = d.OrderID
where d.Status like 'Not Delivered';


--x) Show a list of members who made more than 2 orders. The list should show their member id, name, and role(student/staff) and total orders.
select o.MemberID, m.MemberName, m.Role, count(o.OrderID) as [Total Orders] from Member m
inner join MealOrder o
on m.MemberID = o.MemberID
group by o.MemberID, m.MemberName, m.Role
having (select count(o.OrderID)) > 2
order by o.MemberID, m.MemberName, m.Role;


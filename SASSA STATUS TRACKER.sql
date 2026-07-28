CREATE DATABASE SassaTrackerDB;
USE SassaTrackerDB;

CREATE TABLE Applicants (
    IDNumber INT(13) PRIMARY KEY ,
    FullName VARCHAR(50) NOT NULL ,
    PhoneNumber VARCHAR(20) NOT NULL,
    EmailAddress VARCHAR(100) NOT NULL ,

);

CREATE TABLE Applications (
    ApplicationID INT IDENTITY(1,1) PRIMARY KEY,
    IDNumber INT(13) NOT NULL,
    GrantType VARCHAR(50) NOT NULL,
    CurrentStatus VARCHAR(20) DEFAULT 'Pending',
    LastUpdated DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IDNumber) REFERENCES Applicants(IDNumber)
);

CREATE TABLE NotificationLogs (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    ApplicationID INT NOT NULL,
    NotificationType VARCHAR(10) NOT NULL,
    SentTimestamp DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (ApplicationID) REFERENCES Applications(ApplicationID)
);
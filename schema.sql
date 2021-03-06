BEGIN TRANSACTION;
CREATE TABLE Students(St_Id INTEGER PRIMARY KEY AUTOINCREMENT, 
	F_Name TEXT NOT NULL, 
	L_Name TEXT NOT NULL);
INSERT INTO Students VALUES(1, 'John', 'Smith');

CREATE TABLE Quizzes(Q_Id INTEGER PRIMARY KEY AUTOINCREMENT, 
	Subject TEXT NOT NULL, 
	Q_num INTEGER, 
	Date TEXT NOT NULL);
INSERT INTO Quizzes VALUES(1, 'Python Basics', 5, 'February 5, 2015');


CREATE TABLE Results(Score INTEGER PRIMARY KEY,
	Student_ID INTEGER NOT NULL,
	Quiz_ID INTEGER NOT NULL,
        FOREIGN KEY(Student_ID) REFERENCES Students(St_Id),
        FOREIGN KEY(Quiz_Id) REFERENCES Quizzes(Q_Id));
INSERT INTO Results VALUES(85,1,1);

COMMIT;

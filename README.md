Test List Creator For Compa Framework
What is a test list ?
Testlist is a file with *.tl extension for Compa Framework what contains the execution list of testcases. A picture below shows how a testlist looks like.

Why use this program ?

Due to the instability of the Test enviroment false positive tests may appear many times . In example normally 50 failed testcases need to rerun and required to select hand by hand. If there are thousands of testcases this is very annoying. That’s why Test List creator is a good choice in this case. 

How it works ?
The tool is waiting for a test report for first input. It parsing the report and checking what test cases are failed. After reading the second input(an empty testlist) where all tests are skipped. Lot of these are defined in the Database\Testlist folder so You don’t need to create it. 

If You modify the testcases in the variation file (delete some tests, or adding new one). You have to create a new Empty Testlist for the corresponding testpackage.
Finally Select the Path for the Output. And You’re testlist is ready. After You can read the log files for additional information form the \History folder.

 


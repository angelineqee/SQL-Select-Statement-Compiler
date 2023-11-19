## SQL Select Statement - Lexixal and Syntax Analyzer
This is a lexical analyzer and a parser implemented in Python for the purpose of CPT316 Assignment 1. The language that is accepted by the compiler is SQL Select statement, with some limitations and exceptions. The concept of Recursive Decent Parser is implemented through recursive function call.

## Built with
Visual Studio Code [https://code.visualstudio.com/]

## Prerequisites
Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

## Getting Started
1.  Clone the project repository to your local machine.
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   ```
2. There are 2 files in this project: SQL-Select-Statement-Compilation and test.txt.
Lexical-parser.py is the source code written in Python.
test.txt contains the test input, SQL SELECT statement, to the program. (Note: Only one SELECT statement can be parsed to the program each time)
You may rewrite the test.txt file to test the output for different inputs.

3. Replace the file path to the test.txt in the source code at line 171.
```
text = open('YourFilePath','r')
``` 
4. You may run the source code on your preferred IDE or

### Running the Python Script

Follow these steps to run the Python script:

1. Open a terminal or command prompt.

2. Navigate to the directory where the Python script is located.

   ```bash
   cd path/to/your/project
   ```
   Run the Python script using the following command:
   ```bash
   python example.py
   ```
   If you're using Python 3, you may need to use python3 instead:
   ```bash
   python3 example.py
   ```

## Acknowledgments
This is a group project with 4 members: Ooi Yue Sheng, Jee Rou Yi, LeeJu Yi, Angeline Teoh Qee

# Compiler
Author: Eduardo Mendez Santa Ana

### Before Running
Make sure to install all the dependencies listed in [requirements.txt](https://github.com/EduardoMSA/compilers-project/blob/master/requirements.txt).

You can install them by running `pip install -r requirements.txt` in your shell.

### Running Compiler
The python program you need to run is [compiler.py](https://github.com/EduardoMSA/compilers-project/blob/master/compiler.py).

It accepts up to 2 additonal command line arguments.

The first argument indicates the path to the file that will be compiled.

	- `python compiler.py input.txt`

The second argument indicates the path to the file that will contained the compiled code.

	- `python compiler.py input.txt output.txt`

Both parameters are optional, in case you don't specify the second parameter the compiled code will be written by default in `output.txt`. If you don't specify the first parameter, the program will attempt to compile the file [`input.txt`](https://github.com/EduardoMSA/compilers-project/blob/master/input.txt) if exists. It is possible to run the compiler with the following command:

	- `python compiler.py`
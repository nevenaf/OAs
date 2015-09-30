# OAs

This is an integer program for construction of small size orthogonal, covering and packing arrays in reduced form. It was meant for construction of orthogonal arrays in reduced form, and as such, the number of columns can be at most one more than the number of symbols.

=====
**Downloading source code and execution**

Download the source code by:
```
  git clone https://github.com/nevenaf/OAs.git
```
This will create a folder called OAs in your current directory. To start the program, execute:
```
cd OAs
python find_oa.py
```
=====

**Recquired packages**

[Gurobi](http://www.gurobi.com/) optimization library is used for linear and integer programs. Gurobi offers a free academic license. The following links offer more information about how to install Gurobi and obtain a license can be found in the [quick start guide](http://www.gurobi.com/documentation/5.6/quickstart/).

====

**Input options**

First, you are prompted to enter the number of columns and symbols. Note that **the number of columns can be at most one more than the number of symbols** in the current version. This is because the program is primarily meant for finding optimal orthogonal arrays in reduced form.

We give a short description for the other options:
* [packing, covering, oa]: In a packing (covering), every ordered pair of symbols occures at most (at least) once in every pair of columns. An orthogonal array has every pair covered exactly once.
* [L,I]: An array is constructed by an integer program (I), but one can also get the result of its linear relaxation (L).
* Execution time: Integer programs can run for extremely long time. The default is one hour.
* There is also an option to enter a subset of rows which must be contained in the array. The rows should be saved in an array in a .p file. User is prompted for the directory and the name of the file in which the subarray is sorted. For example, in an array with 4 columns and at least 5 symbols, the following may be a subarray. One way to save it in the appropreat format is the following:
```
import cPickle as pickle
subarray = [[1,0,1,3],[2,0,2,4],[3,0,3,1]]
pickle.dump(subarray, open('subarray_file.p', 'w'))
```
Note that the final array is meant to be in reduced form. By default, it contains rows of the form 0xxxxxx where x is any symbol.



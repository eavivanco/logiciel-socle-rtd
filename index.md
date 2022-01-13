## Welcome to the GitHub Page of Esteban's python project

Whit every commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

# Accounting files filler software

[Read the docs link](https://readthedocs.org/projects/eavivanco-logiciel-socle-rtd/)

## Description

### What is it ?

A simple software that makes the automates the task of filling banking movements details

### How does it work ?

1. For setting up the software you just have to introduce once the details of the banking movements that links certain movement to certain kind of relation with your company
eg : I know the id : 197944846 is linked to a CLIENT, so I introduce '197944846' to the client's list
2. You upload the .csv/.xlsx file you need to fill into the path /src/in/yourfile.csv
3. You take the filled file from /src/out/yourfilledfile.csv (as .csv o .xlsx)
4. You add new relations if needed
eg : A new client with id : 136710605 is linked to a CLIENT, so I introduce '136710605' to the client's list

### Who will use this software ?

The person in charge of finance who has to report the banking movements to the accountant

### What is the goal of this project ?

Save valuable time for the person in charge of finance, automating repetitive task which is also sensitive to typing errors

## License information

Creative Commons **BY-NC-SA**

- Copy & Publish permitted 
- Attribution required
- Non-Comercial use only
- Modifications & Adaptations permitted
- Licence changes forbidden

## Contact information

Esteban VIVANCO -> eavivanco@uc.cl

## Technical documentation

Library required : pandas

### Execution

The execution file is /src/main.py, where you can define :
- Folder name as client
- Input file name as file_name

### Functions

The functions used in main.py are contained in the file /src/functions.py and are the following :

#### processor(xls, client)

It receives xls and client as parameters 

This is the main function, using the functions 
1. cleaner(df)
2. filler(df_filt, index)
3. output(df_mask, df_filled, index)

#### cleaner(df)

It receives the .csv file imported as a data frame and standarizes transaccions details given by the bank, deleting punctuations, spaces and some special characters.

output : 
- clean data frame
- index where the filler has to start and end to fill the file

#### filler(df_filt, index)

It receives the "clean" data frame and the index from the cleaner and fills the information of interest. One of its components is the function ```egresos(df_filt, pos)``` which groups the different outcomes of the company, for 
example, the function proveedores(df_filt, pos) (suppliers) which contains the list :

- proveedores = \["mantencion", "transf", "entel", "servicios", "77030755", "77030117"\]

with key words that links the bank description to the key word "Pago Proveedores", required by the accountant. If is needed to add more suppliers, the user just have to add a keyword to this list.

#### output(df_mask, df_filled, index)

It receives the "filled" data frame from the filler, with the index from the cleaner and a mask (original data frame) in order to create a final .csv/.xlsx file in /src/out/yourfilledfile.csv

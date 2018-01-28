#Class: CS-470
#Instructor: Mahesh Maddumala
#Name: Nathaniel Barnett
#Student ID: 16208536
#Assignment: Assignment 1 
#Date: 01/26/18

#Algorithm: 1. prompt user for action:
#           - create schema (minimum of 2)
#           - Update DB
#           - Retrieve data from specified DB
#           2. if schema not stored, then create schema
#               if schema stored, then return to menu or prompt to write new schema
#           
###########################################################################################
### Imports
import glob
import os

### UTILITY FUNCTIONS
def _clearSchema_():
        for file in glob.glob('*.csv'):
            if 'schema' in file.lower():
                os.remove(file)

        print('\n' + '*' * 5 + 'ALL SCHEMAS CLEARED'.upper() + '*' * 5)

def displayMenu():
    print('\n' + 5 * '*' + 'Database Management System' + 5 * '*' + '\n')
    print('1. Create Schema\n')
    print('2. Update A Database\n')
    print('3. Update Data In A Database\n')
    print('4. Retrieve Data From A Database\n')
    print('5. Exit Database Management System\n')

def addSchema():
    newSchema = []
    schemaFlag = True
    while schemaFlag:
        print('\nThis will add a schema to the saved list of schemas.\n')
        print('Enter each field header name for the schema, and seperate each field by a ","\n')
        print('After entering all fields for the new Database, hit ENTER.\n')
        schemaString = input().strip().strip(',')
        newSchema = schemaString.split(",")
        if len(newSchema) < 2:
            print( '\n' + 5 * '*' +'SCHEMA NEEDS MORE HEADER FIELDS' + 5 * '*' + '\n')
            continue
        else:
            schemaFlag = False

    dbNameFlag = True
    while dbNameFlag:
        print("Enter name of database. Example: 'Student Roster'")
        dbTitle = input().upper().strip()
        prompt = input("Is this database name correct? ENTER 'Y' or 'N'").upper()
        if (prompt == 'Y'):
            dbNameFlag = False
        elif (prompt == 'N'):
            dbNameFlag = True
            continue
        else:
            continue
        
    schemaCounter = len(checkForSchema())
    fileName = dbTitle + '_schema.csv'
    schemaFile = open(fileName, 'w')
    schemaFile.write(schemaString.upper().rstrip(','))

    schemaFile.close()
    print('\n' + 5 * '*' + 'New schema added to storage'.upper() + 5 * '*' + '\n')


def checkForSchema(ending='*.csv'):
    """" Returns a list of files with 'ending'. Returns empty list if no files with that ending. """
    
    tempSchemaMaps = []
    for file in glob.glob(ending):
        if 'schema' in file.lower():
            tempSchemaMaps.append(file)
        
    return tempSchemaMaps

def updateDatabaseSchema():
    currentSchema = checkForSchema()
    schemaFiles = []
    print('\n' + 5 * '*' + 'Select A Database' + 5 * '*' + '\n')

    dbFlag = True
    while dbFlag:
        counter = -1
        for db in currentSchema:
            counter = counter + 1
            print( str(counter) + '. ' + db.rstrip('_schema.csv'))
            schemaFiles.append(db)
            

        dbChoice = input().strip()
        
        try:
            dbChoice = int(dbChoice)
            if (dbChoice > counter or dbChoice < 1):
                print('\nValue entered is not associated with a database on file.\n'.upper())
                continue
        except ValueError:
            print('\nValue entered is not an integer. Please enter an integer associated with a database.')
            continue
        
            

        dbFlag = False

    file = open(schemaFiles[dbChoice], 'r')
    file.seek(0)
    prevSchema = file.readline()
    file.close()
    
    dbFlag = True
    while dbFlag:
        print('\nPREVIOUS SCHEMA: ' + prevSchema + '\n')
        print('\n1. Keep this Schema, and append to the end of schema.\n' +
              '2. Remove this schema, and insert new schema.\n'
              '3. Keep this schema, do not update database.\n')
        prompt = input().strip()
    
        try:
            prompt = int(prompt)
            if (prompt > 3 or prompt < 1):
                print("\nValue entered is not a menu option. Please enter a menu option.\n")
            dbFlag = False
        except ValueError:
            print('\nValue entered is not an integer. Please enter an integer associated with a database.\n')
        
            
    #1. Append to prev schema
    if prompt == 1:
        newSchema = []
        prevDB = []
        prevDBFile = open(schemaFiles[dbChoice], 'r')
        prevDBFile.seek(0)
        prevDB = prevDBFile.readlines()
        prevDBFile.close()
        
        schemaFlag = True
        print('Enter each field header name for the schema, and seperate each field by a ","\n')
        print('After entering all fields for the new headers to be added to database, hit ENTER.\n')
        schemaString = input().upper()
        DBFile = open(schemaFiles[dbChoice], 'w')
        for i in range(len(prevDB)):
            if i == 0:
                DBFile.write((prevDB[i] + ',' + schemaString).rstrip(','))
                continue
            DBFile.writeline(prevDB[i])

        DBFile.close()
        print('\n '+ 5 * '*' + 'Schema Updated' + 5 * '*' + '\n')

    #2. Remove schema, and add new schema
    elif prompt == 2:
        warning = 'g'
        while (warning != 'Y' or warning != 'N'):
            warning = input('\nWARNING: changing the schema of apreviously defined database may result in a corrupted database. \n'
                        + 'Meaning, the newly inserted schema may not accurately define or relate to teh previously stored data. \n'
                        + 'Do you wish to proceed? ENTER "Y" OR "N"\n').upper()
            if warning == 'N':
                print('\n '+ 5 * '*' + 'Schema Not Updated' + 5 * '*' + '\n')
                return
            elif warning == 'Y':
                break
        
        newSchema = []
        prevDB = []
        prevDBFile = open(schemaFiles[dbChoice], 'r')
        prevDBFile.seek(0)
        prevDB = prevDBFile.readlines()
        prevDBFile.close()
        
        schemaFlag = True
        print('Enter each field header name for the schema, and seperate each field by a ","\n')
        print('After entering all fields for the new schema to be added to database, hit ENTER.\n')
        schemaString = input().upper().strip()
        DBFile = open(schemaFiles[dbChoice], 'w')
        for i in range(len(prevDB)):
            if i == 0:
                DBFile.write(schemaString.rstrip(','))
                continue
            DBFile.writeline(prevDB[i])

        DBFile.close()
        print('\n '+ 5 * '*' + 'Schema Updated' + 5 * '*' + '\n')

    # 3. Keep this schema
    elif prompt == 3:
        print('\n '+ 5 * '*' + 'Schema Not Updated' + 5 * '*' + '\n')
        return


def updateData():
    pass


def retrieveDatabase():
    pass


### END OF UTILITY FUCTIONS
###########################################################################################

schemamaps = []
choice = int
flag = True
while flag:
    displayMenu()
    choice = input()
    if choice == '1': # Create Schema
        addSchema()
              
    elif choice == '2': # Update a database schema
        updateDatabaseSchema()
    elif choice == '3': # Update data in database
        pass
    elif choice == '4': # retrieve data from a database
        pass
    elif choice == '5': # exit form program
        flag = False
        pass
    else:
        print("\nNot a valid menu option. Please select an option 1 - 5.\n")
    



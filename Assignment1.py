

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
#import numpy

### UTILITY FUNCTIONS
def _clearDBS_():
        for file in glob.glob('*.csv'):
            if 'schema' in file.lower():
                tempFile = open(file, 'w')
                tempFile.close()

            if '_DB.csv' in file:
                os.remove(file)

        print('\n' + '*' * 5 + 'ALL SCHEMAS/DATABASES CLEARED'.upper() + '*' * 5)

def displayMenu():
    print('\n' + 5 * '*' + 'Database Management System' + 5 * '*' + '\n')
    print('1. Create Schema\n')
    print('2. Update A Schema\n')
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
        
    #schemaCounter = len(checkForSchema())
    dbFileName = dbTitle + '_DB.csv'
    dbFile = open(dbFileName, 'w')
    dbFile.close()
    schemaFileName = '_schemaMaster_.csv'
    try:
        schemaFile = open(schemaFileName, 'a')
    except FileNotFoundError:
        schemaFile = open(schemaFileName, 'w')
    schemaFile.write(schemaString.upper().rstrip(',')) # append schema to MASTER LIST
    schemaFile.write(',' + dbFileName + '\n')

    schemaFile.close()
    print('\n' + 5 * '*' + 'New schema added to storage'.upper() + 5 * '*' + '\n')


def checkForSchema(DBOnly=False, ending='*.csv'):
    """" Returns a list of files with 'ending'. Returns empty list if no files with that ending. """
    tempSchemaMaps = []
    try:
        file = open('_schemaMaster_.csv', 'r')
    except FileNotFoundError:
        print('\n' + 5 * '*' + 'No Initialized Schema Found' + 5 * '*' + '\n')
        return tempSchemaMaps
    
    for line in file:
        if (DBOnly == True):
            tempLine = line.split(',')
            tempSchemaMaps.append(tempLine[len(tempLine) - 1])

        else:
            tempSchemaMaps.append(line)

    if (len(tempSchemaMaps) == 0):
        print('\n' + 5 * '*' + 'No Initialized Schema Found' + 5 * '*' + '\n')
        
    return tempSchemaMaps


def selectDB():
    currentDB = checkForSchema(True,)
    schemaFiles = []
    print('\n' + 5 * '*' + 'Select A Database' + 5 * '*' + '\n')

    dbFlag = True
    while dbFlag:
        counter = 0
        for db in currentDB:
            counter = counter + 1
            print( str(counter) + '. ' + db.split('_')[0] + '\n')
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
        dbChoice = dbChoice - 1 # to set counter to the index of list.
        return dbChoice
        

def updateDatabaseSchema():
    schemaFiles = checkForSchema()
    if (len(schemaFiles) == 0):
        return
    dbChoice = selectDB();
    schemaParse = schemaFiles[dbChoice].split(',')
    prevSchema = schemaParse[:len(schemaParse) - 1] # counting starts at 0, and dropping last elem.
    prevSchemaFH = schemaParse[len(schemaParse) - 1]
    prevSchemaStr = ''
    for elem in prevSchema:
        prevSchemaStr = prevSchemaStr + elem + ','

    dbFlag = True
    while dbFlag:
        print('\nPREVIOUS SCHEMA: ' + prevSchemaStr.strip(',') + '\n')
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
        


    newSchema = []
    prevSchemas = []
    prevSchemaFile = open('_schemaMaster_.csv', 'r')
    prevSchemaFile.seek(0)
    prevSchemas = prevSchemaFile.readlines()
    prevSchemaFile.close()
    #1. Append to prev schema
    if prompt == 1:
        
        schemaFlag = True
        print('WARNING: Changing schema will result in an inaccurate database.\n')
        print('When retrieving database, any schema fields that were added may not display correctly.\n')
        print('\nEnter each field header name for the schema, and seperate each field by a ","\n')
        print('After entering all fields for the new headers to be added to database, hit ENTER.\n')

        schemaString = input().upper()
        try:
            schemaFile = open('_schemaMaster_.csv', 'w')
            for i in range(len(prevSchemas)):
                if i == (dbChoice):
                    schemaFile.write((prevSchemaStr.strip(',') + ',' + schemaString).strip(',') + ',' + prevSchemaFH)
                else:    
                    schemaFile.write(prevSchemas[i])

            schemaFile.close()
        except FileNotFoundError:
            schemaFile.close()
            print('EXCEPTION')
        print('\n '+ 5 * '*' + 'Schema Updated' + 5 * '*' + '\n')

    #2. Remove schema, and add new schema
    elif prompt == 2:
        warning = 'g' #DUMMY VALUE to start while loop
        while (warning != 'Y' or warning != 'N'):
            warning = input('\nWARNING: changing the schema of a previously defined database may result in a corrupted database. \n'
                        + 'Meaning, the newly inserted schema may not accurately define or relate to teh previously stored data. \n'
                        + 'Do you wish to proceed? ENTER "Y" OR "N"\n').upper()
            if warning == 'N':
                print('\n '+ 5 * '*' + 'Schema Not Updated' + 5 * '*' + '\n')
                return
            elif warning == 'Y':
                break
        
        
        print('Enter each field header name for the schema, and seperate each field by a ","\n')
        print('After entering all fields for the new schema to be added to database, hit ENTER.\n')
        schemaString = input().upper().strip()
        schemaFile = open('_schemaMaster_.csv', 'w')
        for i in range(len(prevSchemas)):
            if i == (dbChoice):
                schemaFile.write(schemaString.rstrip(',') + ',' + schemaParse[len(schemaParse) - 1])
                continue
            schemaFile.write(prevSchemas[i])

        schemaFile.close()
        print('\n '+ 5 * '*' + 'Schema Updated' + 5 * '*' + '\n')

    # 3. Keep this schema
    elif prompt == 3:
        print('\n '+ 5 * '*' + 'Schema Not Updated' + 5 * '*' + '\n')
        return


def updateData():
    DBS, schemaMaps = _getDBS()
    dbChoice = selectDB()

    flag = True
    while flag:
        newData = input('\nEnter data to be added to database, and separate each field by "," then hit ENTER.\n')
        newData.upper()
        correct = input('\nIs the new data correct? ENTER "Y" or "N"\n').upper()
        if (correct == 'Y'):
            flag = False
        else:
            continue

    readCurrentDB = open(DBS[dbChoice], 'r')
    arrayDB = []
    for line in readCurrentDB:
        tempLine = line.strip() + '\n'
        arrayDB.append(tempLine)
    readCurrentDB.close()
    newData = newData.strip(',').strip(' ').upper()
    arrayDB.append(newData)
    writeCurrentDB = open(DBS[dbChoice],'w')

    writeCurrentDB.writelines(arrayDB)

    writeCurrentDB.close()

    print('\n' + 5 * '*' + 'DATABASE UPDATED' + 5 * '*' + '\n')




def _getDBS():
    schemas = checkForSchema()
    DBS = []
    schemaMaps = []
    for schema in schemas:
        DBS.append(schema.split(',')[-1].strip())
        schemaMaps.append(schema.split(','))

    return (DBS, schemaMaps)

def _printDB(DBfilename, lineSelect = False):
    currentDB = open(DBfilename, 'r')
    arrayDB = []
    maxWordLen = 0
    flag = 1
    for line in currentDB:
        tempLine = str(flag) + ': ' + line.strip()
        tempList = tempLine.split(',')
        arrayDB.append(tempList)
        flag = flag + 1
        for item in tempList:
            if (len(item) > maxWordLen):
                maxWordLen = len(item)

    currentDB.close()
    colWidth = maxWordLen + 2  # padding
    tempDBS, schemamaps = _getDBS()
    currentSchema = ''
    for schema in schemamaps:
        if (schema[-1].strip() == DBfilename):
            currentSchema = schema[:-1]

    rID = 0
    print('\n' + 10 * '*' + 'DATABASE: ' + DBfilename.split('_')[0] + ' ' + 10 * '*' + '\n')
    for row in arrayDB:
        cID = 0

        if (rID == 0):
            column = 0
            for col in currentSchema:
                print(currentSchema[column].ljust(colWidth), end='')
                column += 1
            print('\n', end='')


        for col in arrayDB[rID]:
            print(arrayDB[rID][cID].ljust(colWidth), end='')
            if (cID < len(row) - 1):
                cID = cID + 1

        if (rID < len(arrayDB) - 1):
            rID = rID + 1
            print('\n', end='')

    print()



def retrieveDatabase():
    DBS, schemaMaps = _getDBS()

    dbChoice = selectDB()
    _printDB(DBS[dbChoice])
    

    ### Function to print database info


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
        updateData()
    elif choice == '4': # retrieve data from a database
        retrieveDatabase()
    elif choice == '5': # exit form program
        flag = False
        pass
    else:
        print("\nNot a valid menu option. Please select an option 1 - 5.\n")
    



# Creating and managing DynamoDB tables

For DynamoDB management I have selected the `.Net` AWS SDK. A CLI tool is created with which the table and the items in it can be managed.

## Prerequisites

To use the .NET AWS SDK, you'll need to have the following prerequisites installed:

- .NET Framework

You can download the .NET Framework from the official Microsoft website:

- .NET Framework: https://dotnet.microsoft.com/download/dotnet-framework

Once you have the necessary prerequisites installed, you can use the .NET AWS SDK to create and manage DynamoDB tables.

## Execution

1. Open a command prompt or terminal.
2. Change the directory to the `dynamodb` folder.

To execute the tool, use the following command:

```
dotnet run -- -?
```

This will display the help information for the tool.

### Commands
- `create`: Create the `Bookshelf` table in DynamoDB.
- `delete`: Delete the `Bookshelf` table from DynamoDB.
- `delete-item`: Delete an item from the `Bookshelf` table based on primary key.
- `insert`: Insert a new item into the `Bookshelf` table.
- `list`: List all items in the `Bookshelf` table.
- `query`: Query the `Bookshelf` table for a specific author.
- `update`: Update an item in the `Bookshelf` table.

### Required command for the demo

First of all you need to create the `Bookcshelf` table:
```
dotnet run -- create
```

To insert the 30 famous books into the Bookshelf table, use the `books.bat` command located in the `dynamodb` folder. 

You can then use the other commands to `query`, `update`, and `delete items` from the table.
using System;
using System.Threading.Tasks;
using Amazon;
using Amazon.Util;
using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.Model;
using Amazon.Runtime;
using McMaster.Extensions.CommandLineUtils;

namespace BookshelfCli
{
    [Command(Name = "bookshelf", Description = "CLI tool for managing Bookshelf table in DynamoDB")]
    [Subcommand(
        typeof(CreateTableCommand),
        typeof(DeleteTableCommand),
        typeof(InsertItemCommand),
        typeof(ListItemsCommand),
        typeof(QueryAuthorCommand),
        typeof(UpdateItemCommand),
        typeof(DeleteItemCommand))]
    public class BookshelfCli
    {

        public static async Task<int> Main(string[] args) => await CommandLineApplication.ExecuteAsync<BookshelfCli>(args);

        private async Task<int> OnExecuteAsync(CommandLineApplication app, IConsole console)
        {
            console.WriteLine("Please specify a subcommand.");
            app.ShowHelp();
            return 1;
        }
    }
}

using System;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;
using Amazon;
using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.Model;
using Amazon.Runtime;
using Amazon.Runtime.CredentialManagement;
using McMaster.Extensions.CommandLineUtils;

[Command(Name = "delete-item", Description = "Delete an item from the Bookshelf table based on primary key")]
public class DeleteItemCommand
{
    [Option(Description = "AWS region where the table exists", ShortName = "r")]
    public string Region { get; set; }

    [Option(Description = "Author of the book", ShortName = "a", LongName = "author", ValueName = "AUTHOR")]
    [Required]
    public string Author { get; set; }

    [Option(Description = "Title of the book", ShortName = "t", LongName = "title", ValueName = "TITLE")]
    [Required]
    public string Title { get; set; }

    [Obsolete]
    public async Task<int> OnExecuteAsync(IConsole console)
    {
        try
        {
            var profile = new CredentialProfileStoreChain().TryGetProfile("default", out var profileResult)
                ? profileResult
                : throw new Exception("AWS profile not found.");
            var region = RegionEndpoint.GetBySystemName(profile.Region.SystemName);
            var awsProfile = Environment.GetEnvironmentVariable("AWS_PROFILE");
            if (string.IsNullOrEmpty(awsProfile))
            {
                throw new Exception("AWS profile not found in AWS_PROFILE environment variable.");
            }

            var credentials = new StoredProfileAWSCredentials(awsProfile);
            var client = new AmazonDynamoDBClient(credentials, region);

            var key = new Dictionary<string, AttributeValue>
            {
                { "author", new AttributeValue(Author) },
                { "title", new AttributeValue(Title) }
            };

            var request = new DeleteItemRequest
            {
                TableName = "Bookshelf",
                Key = key,
                ReturnValues = ReturnValue.ALL_OLD
            };

            var response = await client.DeleteItemAsync(request);

            if (response.Attributes != null && response.Attributes.Count > 0)
            {
                console.WriteLine($"Item {Title} by {Author} was deleted successfully from the Bookshelf table.");
            }
            else
            {
                console.WriteLine($"Item {Title} by {Author} was not found in the Bookshelf table.");
            }

            return 0;
        }
        catch (Exception ex)
        {
            console.Error.WriteLine(ex.Message);
            return 1;
        }
    }
}

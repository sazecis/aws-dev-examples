using System;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;
using Amazon;
using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.DocumentModel;
using Amazon.DynamoDBv2.Model;
using Amazon.Runtime;
using Amazon.Runtime.CredentialManagement;
using McMaster.Extensions.CommandLineUtils;

[Command(Name = "insert", Description = "Insert a new item into the Bookshelf table")]
public class InsertItemCommand
{
    [Option(Description = "AWS region where the table exists", ShortName = "r")]
    public string Region { get; set; }

    [Option(Description = "Author of the book", ShortName = "a", LongName = "author", ValueName = "AUTHOR")]
    [Required]
    public string Author { get; set; }

    [Option(Description = "Title of the book", ShortName = "t", LongName = "title", ValueName = "TITLE")]
    [Required]
    public string Title { get; set; }

    [Option(Description = "Type of the book", ShortName = "y", LongName = "type", ValueName = "TYPE")]
    [Required]
    public string Type { get; set; }

    [Option(Description = "Description of the book", ShortName = "d", LongName = "description", ValueName = "DESCRIPTION")]
    public string Description { get; set; }

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

            var request = new PutItemRequest
            {
                TableName = "Bookshelf",
                Item = new Dictionary<string, AttributeValue>
                {
                    { "author", new AttributeValue(Author) },
                    { "title", new AttributeValue(Title) },
                    { "type", new AttributeValue(Type) }
                }
            };

            if (!string.IsNullOrEmpty(Description))
            {
                request.Item.Add("description", new AttributeValue(Description));
            }

            await client.PutItemAsync(request);

            console.WriteLine($"Item {Title} by {Author} added successfully to the Bookshelf table.");
            return 0;
        }
        catch (Exception ex)
        {
            console.Error.WriteLine(ex.Message);
            return 1;
        }
    }
}

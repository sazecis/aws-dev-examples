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

[Command(Name = "update", Description = "Update an item in the Bookshelf table")]
public class UpdateItemCommand
{
    [Option(Description = "AWS region where the table exists", ShortName = "r")]
    public string Region { get; set; }

    [Option(Description = "Author of the book", ShortName = "a", LongName = "author", ValueName = "AUTHOR")]
    [Required]
    public string Author { get; set; }

    [Option(Description = "Title of the book", ShortName = "t", LongName = "title", ValueName = "TITLE")]
    [Required]
    public string Title { get; set; }

    [Option(Description = "New category of the book", ShortName = "y", LongName = "new-category", ValueName = "NEW_CATEGORY")]
    public string NewCategory { get; set; }

    [Option(Description = "New description of the book", ShortName = "d", LongName = "new-description", ValueName = "NEW_DESCRIPTION")]
    public string NewDescription { get; set; }

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

            var itemKey = new Dictionary<string, AttributeValue>
            {
                { "author", new AttributeValue(Author) },
                { "title", new AttributeValue(Title) }
            };

            var existingItem = await client.GetItemAsync("Bookshelf", itemKey);
            if (existingItem.Item.Values.Count == 0)
            {
                console.Error.WriteLine($"Item with author '{Author}' and title '{Title}' not found in the Bookshelf table.");
                return 1;
            }

            var updateExpression = "SET ";
            var expressionAttributeValues = new Dictionary<string, AttributeValue>();
            var expressionAttributeNames = new Dictionary<string, string>();

            if (!string.IsNullOrEmpty(NewCategory))
            {
                updateExpression += "#y = :newCategory, ";
                expressionAttributeValues.Add(":newCategory", new AttributeValue(NewCategory));
                expressionAttributeNames.Add("#y", "category");
            }

            if (!string.IsNullOrEmpty(NewDescription))
            {
                updateExpression = updateExpression + "#desc = :desc";
                expressionAttributeNames["#desc"] = "description";
                expressionAttributeValues[":desc"] = new AttributeValue(NewDescription);
            }

            var request = new UpdateItemRequest
            {
                TableName = "Bookshelf",
                Key = new Dictionary<string, AttributeValue>
                {
                    { "author", new AttributeValue(Author) },
                    { "title", new AttributeValue(Title) }
                },
                UpdateExpression = updateExpression,
                ExpressionAttributeNames = expressionAttributeNames,
                ExpressionAttributeValues = expressionAttributeValues
            };

            await client.UpdateItemAsync(request);

            console.WriteLine($"Item {Title} by {Author} updated successfully in the Bookshelf table.");
            return 0;
        }
        catch (Exception ex)
        {
            console.Error.WriteLine($"Error updating item: {ex}");
            return 1;
        }
    }
}
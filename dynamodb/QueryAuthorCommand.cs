using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;
using Amazon;
using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.DocumentModel;
using Amazon.DynamoDBv2.Model;
using Amazon.Runtime;
using Amazon.Runtime.CredentialManagement;
using McMaster.Extensions.CommandLineUtils;

[Command(Name = "query", Description = "Query the Bookshelf table for a specific author")]
public class QueryAuthorCommand
{
    [Option(Description = "AWS region where the table exists", ShortName = "r")]
    public string Region { get; set; }

    [Option(Description = "Author to search for", ShortName = "a", LongName = "author", ValueName = "AUTHOR")]
    [Required]
    public string Author { get; set; }

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

            var request = new QueryRequest
            {
                TableName = "Bookshelf",
                KeyConditionExpression = "author = :v_author",
                ExpressionAttributeValues = new Dictionary<string, AttributeValue>
                {
                    { ":v_author", new AttributeValue(Author) }
                }
            };

            var result = await client.QueryAsync(request);

            console.WriteLine($"Books by {Author}:");
            foreach (var item in result.Items)
            {
                console.WriteLine("- Title: {0}, Type: {1}, Description: {2}", item["title"].S, item["type"].S, item.ContainsKey("description") ? item["description"].S : "");
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

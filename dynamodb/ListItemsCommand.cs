using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Amazon;
using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.Model;
using Amazon.Runtime;
using Amazon.Runtime.CredentialManagement;
using McMaster.Extensions.CommandLineUtils;

[Command(Name = "list", Description = "List all items in the Bookshelf table")]
public class ListItemsCommand
{
    [Option(Description = "AWS region where the table exists", ShortName = "r")]
    public string Region { get; set; }

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

            var request = new ScanRequest
            {
                TableName = "Bookshelf"
            };

            var response = await client.ScanAsync(request);

            console.WriteLine($"Listing items in the Bookshelf table:");
            foreach (var item in response.Items)
            {
                console.WriteLine($"- Author: {item["author"].S}, Title: {item["title"].S}, Type: {item["type"].S}, Description: {(item.ContainsKey("description") ? item["description"].S : "")}");
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

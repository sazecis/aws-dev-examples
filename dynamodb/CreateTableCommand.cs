using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using Amazon;
using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.Model;
using Amazon.Runtime;
using Amazon.Runtime.CredentialManagement;
using McMaster.Extensions.CommandLineUtils;

namespace BookshelfCli
{
    [Command(Name = "create", Description = "Create the Bookshelf table in DynamoDB")]
    public class CreateTableCommand
    {
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

                var request = new CreateTableRequest
                {
                    TableName = "Bookshelf",
                    AttributeDefinitions = new List<AttributeDefinition>
                    {
                        new AttributeDefinition("author", ScalarAttributeType.S),
                        new AttributeDefinition("title", ScalarAttributeType.S)
                    },
                    KeySchema = new List<KeySchemaElement>
                    {
                        new KeySchemaElement("author", KeyType.HASH),
                        new KeySchemaElement("title", KeyType.RANGE)
                    },
                    ProvisionedThroughput = new ProvisionedThroughput
                    {
                        ReadCapacityUnits = 1,
                        WriteCapacityUnits = 1
                    }
                };

                await client.CreateTableAsync(request);

                console.WriteLine("Table created successfully.");
                return 0;
            }
            catch (Exception ex)
            {
                console.Error.WriteLine(ex);
                return 1;
            }
        }
    }
}

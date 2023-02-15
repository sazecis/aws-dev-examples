using System;
using System.Threading.Tasks;
using Amazon;
using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.Model;
using Amazon.Runtime;
using Amazon.Runtime.CredentialManagement;
using McMaster.Extensions.CommandLineUtils;

namespace BookshelfCli
{
    [Command(Name = "delete", Description = "Delete the Bookshelf table from DynamoDB")]
    public class DeleteTableCommand
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

                var request = new DeleteTableRequest { TableName = "Bookshelf" };

                await client.DeleteTableAsync(request);

                console.WriteLine("Table deleted successfully.");
                return 0;
            }
            catch (Exception ex)
            {
                console.Error.WriteLine(ex.Message);
                return 1;
            }
        }
    }
}

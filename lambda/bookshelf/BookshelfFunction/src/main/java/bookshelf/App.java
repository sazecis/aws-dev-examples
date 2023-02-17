package bookshelf;

import java.util.List;
import java.util.Map;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbTable;
import software.amazon.awssdk.enhanced.dynamodb.model.Page;
import software.amazon.awssdk.enhanced.dynamodb.model.PageIterable;
import software.amazon.awssdk.enhanced.dynamodb.model.ScanEnhancedRequest;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;

public class App implements RequestHandler<Map<String, String>, String> {

    private static final DynamoDbTable<Bookshelf> bookshelfTable;
    private static final ObjectMapper objectMapper;

    static {
        String region = System.getenv("AWS_REGION");
        DynamoDbClient ddbClient = DynamoDbClient.builder()
                .region(Region.of(
                        region))
                .build();
        DynamoDbEnhancedClient enhancedClient = DynamoDbEnhancedClient.builder()
                .dynamoDbClient(ddbClient)
                .build();
        bookshelfTable = enhancedClient.table("Bookshelf", Bookshelf.getTableSchema());
        objectMapper = new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);
    }

    @Override
    public String handleRequest(Map<String, String> input, Context context) {
        try {
            ScanEnhancedRequest request = ScanEnhancedRequest.builder().build();
            PageIterable<Bookshelf> response = bookshelfTable.scan(request);
            String jsonOutput = "";
            for (Page<Bookshelf> page : response) {
                List<Bookshelf> bookshelfItems = page.items();
                for (Bookshelf item : bookshelfItems) {
                    jsonOutput += objectMapper.writeValueAsString(item);
                }
            }
            return jsonOutput;

        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}

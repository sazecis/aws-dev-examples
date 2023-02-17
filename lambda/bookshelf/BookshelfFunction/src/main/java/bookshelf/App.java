package bookshelf;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbTable;
import software.amazon.awssdk.enhanced.dynamodb.model.Page;
import software.amazon.awssdk.enhanced.dynamodb.model.PageIterable;
import software.amazon.awssdk.enhanced.dynamodb.model.ScanEnhancedRequest;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;

public class App implements RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {

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
    public APIGatewayProxyResponseEvent handleRequest(final APIGatewayProxyRequestEvent input, final Context context) {
        Map<String, String> headers = new HashMap<>();
        headers.put("Content-Type", "application/json");
        headers.put("X-Custom-Header", "application/json");

        APIGatewayProxyResponseEvent response = new APIGatewayProxyResponseEvent()
                .withHeaders(headers);
        try {
            ScanEnhancedRequest request = ScanEnhancedRequest.builder().build();
            PageIterable<Bookshelf> dynamoDbResponse = bookshelfTable.scan(request);
            String jsonOutput = "";
            for (Page<Bookshelf> page : dynamoDbResponse) {
                List<Bookshelf> bookshelfItems = page.items();
                for (Bookshelf item : bookshelfItems) {
                    jsonOutput += objectMapper.writeValueAsString(item);
                }
            }
            return response
                    .withStatusCode(200)
                    .withBody(jsonOutput.toString());

        } catch (Exception e) {
            return response
                    .withBody(e.getMessage())
                    .withStatusCode(500);
        }
    }
}

import api.GetS3ObjectSample;
import api.PutS3ObjectSample;

public class Main 
{
    /** Put your access key here **/
    private static final String awsAccessKey = "PUT_KEY_HERE";
    
    /** Put your secret key here **/
    private static final String awsSecretKey = "PUT_SECRET_HERE";
    
    private static void testS3()
    {
    	final String regionName = "us-east-1";
    	final String bucketName = "ryanjwaters";
        PutS3ObjectSample.putS3Object(bucketName, regionName, awsAccessKey, awsSecretKey);
        GetS3ObjectSample.getS3Object(bucketName, regionName, awsAccessKey, awsSecretKey);
    }
    
    private static void testCostExplorer()
    {
    	String query = "{\n" +
        		"  \"TimePeriod\": {\n" + 
        		"    \"Start\":\"2019-09-01\",\n" + 
        		"    \"End\": \"2020-05-01\"\n" + 
        		"  },\n" + 
        		"  \"Granularity\": \"MONTHLY\",\n" + 
        		"  \"Filter\": { \n" + 
        		"    \"Dimensions\": {\n" + 
        		"      \"Key\": \"SERVICE\",\n" + 
        		"      \"Values\": [\n" + 
        		"        \"Amazon Simple Storage Service\"\n" + 
        		"      ]\n" + 
        		"    }\n" + 
        		"  },\n" + 
        		"  \"GroupBy\":[\n" + 
        		"    {\n" + 
        		"      \"Type\":\"DIMENSION\",\n" + 
        		"      \"Key\":\"SERVICE\"\n" + 
        		"    },\n" + 
        		"    {\n" + 
        		"      \"Type\":\"TAG\",\n" + 
        		"      \"Key\":\"Environment\"\n" + 
        		"    }\n" + 
        		"  ],\n" + 
        		"   \"Metrics\":[\"BlendedCost\", \"UnblendedCost\", \"UsageQuantity\"]\n" + 
        		"}";
    	
    	CostExplorerCostAndUsage.getCostAndUsage(query, awsAccessKey, awsSecretKey);
    }
    
    public static void main(String[] args) 
    {
    	// Test S3 HTTP API direct
    	// testS3();
    	
    	// Test Cost Explorer API direct
    	testCostExplorer();
    }
}
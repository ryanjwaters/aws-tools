package api;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import util.BinaryUtils;
import util.HttpUtils;
import util.auth.AWS4SignerBase;
import util.auth.AWS4SignerForAuthorizationHeader;

public class CostExplorerCostAndUsage 
{
    public static void getCostAndUsage(String query, String awsAccessKey, String awsSecretKey) 
    {
        URL endpointUrl;
        try {
            endpointUrl = new URL("https://ce.us-east-1.amazonaws.com/");
        } catch (MalformedURLException e) {
            throw new RuntimeException("Unable to parse service endpoint: " + e.getMessage());
        }

        byte[] contentHash = AWS4SignerBase.hash(query);
        String contentHashString = BinaryUtils.toHex(contentHash);
 
        Map<String, String> headers = new HashMap<String, String>();
        headers.put("x-amz-content-sha256", contentHashString);
        headers.put("content-length", 		""+query.length());
        headers.put("Content-Type", 		"application/x-amz-json-1.1");
        headers.put("X-Amz-Target", 		"AWSInsightsIndexService.GetCostAndUsage");
        
        AWS4SignerForAuthorizationHeader signer = new AWS4SignerForAuthorizationHeader(endpointUrl, "POST", "ce", "us-east-1"); // CE always in us-east-1
        String authorization = signer.computeSignature(headers, null, // no query parameters
                                                       contentHashString, awsAccessKey, awsSecretKey);
                
        // Place the computed signature into a formatted 'Authorization' header
        headers.put("Authorization", authorization);
        String response = HttpUtils.invokeHttpRequest(endpointUrl, "POST", headers, query);
        System.out.println("--------- Response content ---------");
        System.out.println(response);
        System.out.println("------------------------------------");
    }
}

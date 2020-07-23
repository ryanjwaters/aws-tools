package api;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import util.HttpUtils;
import util.auth.AWS4SignerBase;
import util.auth.AWS4SignerForAuthorizationHeader;

/**
 * Samples showing how to GET an object from Amazon S3 using Signature V4 authorization.
 */
public class GetS3ObjectSample {
    
    public static void getS3Object(String bucketName, String regionName, String awsAccessKey, String awsSecretKey) {
    	
        System.out.println("*******************************************************");
        System.out.println("*  Executing sample 'GetObjectUsingHostedAddressing'  *");
        System.out.println("*******************************************************");
        
        URL endpointUrl;
        try {
            endpointUrl = new URL("https://" + bucketName + ".s3.amazonaws.com/ExampleObject.txt");
        } catch (MalformedURLException e) {
            throw new RuntimeException("Unable to parse service endpoint: " + e.getMessage());
        }
        
        Map<String, String> headers = new HashMap<String, String>();
        headers.put("x-amz-content-sha256", AWS4SignerBase.EMPTY_BODY_SHA256);
        
        AWS4SignerForAuthorizationHeader signer = new AWS4SignerForAuthorizationHeader(endpointUrl, "GET", "s3", regionName);
        String authorization = signer.computeSignature(headers, null, // no query parameters
                                                       AWS4SignerBase.EMPTY_BODY_SHA256, awsAccessKey, awsSecretKey);
                
        headers.put("Authorization", authorization);
        String response = HttpUtils.invokeHttpRequest(endpointUrl, "GET", headers, null);
        System.out.println("--------- Response content ---------");
        System.out.println(response);
    }
}

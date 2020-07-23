package waters.ryan.sample.httpapi;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import waters.ryan.sample.util.BinaryUtils;
import waters.ryan.sample.util.HttpUtils;
import waters.ryan.test.sample.auth.AWS4SignerBase;
import waters.ryan.test.sample.auth.AWS4SignerForAuthorizationHeader;

/**
 * Sample code showing how to PUT objects to Amazon S3 with Signature V4 authorization
 */
public class PutS3ObjectSample {
    
    private static final String objectContent = 
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc tortor metus, sagittis eget augue ut,\n"
            + "feugiat vehicula risus. Integer tortor mauris, vehicula nec mollis et, consectetur eget tortor. In ut\n"
            + "elit sagittis, ultrices est ut, iaculis turpis. In hac habitasse platea dictumst. Donec laoreet tellus\n"
            + "at auctor tempus. Praesent nec diam sed urna sollicitudin vehicula eget id est. Vivamus sed laoreet\n"
            + "lectus. Aliquam convallis condimentum risus, vitae porta justo venenatis vitae. Phasellus vitae nunc\n"
            + "varius, volutpat quam nec, mollis urna. Donec tempus, nisi vitae gravida facilisis, sapien sem malesuada\n"
            + "purus, id semper libero ipsum condimentum nulla. Suspendisse vel mi leo. Morbi pellentesque placerat congue.\n"
            + "Nunc sollicitudin nunc diam, nec hendrerit dui commodo sed. Duis dapibus commodo elit, id commodo erat\n"
            + "congue id. Aliquam erat volutpat.\n";
    
    /**
     * Uploads content to an Amazon S3 object in a single call using Signature V4 authorization.
     */
    public static void putS3Object(String bucketName, String regionName, String awsAccessKey, String awsSecretKey) {

        URL endpointUrl;
        try {
            if (regionName.equals("us-east-1")) {
                endpointUrl = new URL("https://s3.amazonaws.com/" + bucketName + "/ExampleObject.txt");
            } else {
                endpointUrl = new URL("https://s3-" + regionName + ".amazonaws.com/" + bucketName + "/ExampleObject.txt");
            }
        } catch (MalformedURLException e) {
            throw new RuntimeException("Unable to parse service endpoint: " + e.getMessage());
        }
        
        byte[] contentHash = AWS4SignerBase.hash(objectContent);
        String contentHashString = BinaryUtils.toHex(contentHash);
        
        Map<String, String> headers = new HashMap<String, String>();
        headers.put("x-amz-content-sha256", 	contentHashString);
        headers.put("content-length", 			"" + objectContent.length());
        headers.put("x-amz-storage-class", 		"REDUCED_REDUNDANCY");
        
        AWS4SignerForAuthorizationHeader signer = new AWS4SignerForAuthorizationHeader(endpointUrl, "PUT", "s3", regionName);
        String authorization = signer.computeSignature(headers, null, // no query parameters
        												contentHashString, awsAccessKey, awsSecretKey);
                
        headers.put("Authorization", authorization);
        String response = HttpUtils.invokeHttpRequest(endpointUrl, "PUT", headers, objectContent);
        System.out.println("--------- Response content ---------");
        System.out.println(response);
    }
}
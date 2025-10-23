/**
 * @file aws-s3-misconfig.ts
 * @description Conceptual TypeScript code illustrating how to identify a misconfigured public S3 bucket.
 *              This is for educational purposes only.
 */

// --- Scenario: Publicly Accessible AWS S3 Bucket ---
// An AWS S3 bucket intended for private storage or internal use
// is accidentally configured to be publicly accessible, potentially
// exposing sensitive data.

// --- Conceptual AWS SDK for JavaScript (v3) Usage ---
// This code is illustrative and would typically run in a Node.js environment
// with appropriate AWS credentials configured.

import { S3Client, GetBucketPolicyCommand, GetPublicAccessBlockCommand, GetBucketAclCommand } from "@aws-sdk/client-s3";

interface BucketSecurityStatus {
    bucketName: string;
    isPubliclyAccessible: boolean;
    publicAccessBlockConfig?: any;
    bucketPolicy?: any;
    aclGrants?: any;
    findings: string[];
}

async function checkS3BucketPublicAccess(bucketName: string): Promise<BucketSecurityStatus> {
    const client = new S3Client({ region: "us-east-1" }); // Replace with your target region
    const status: BucketSecurityStatus = {
        bucketName,
        isPubliclyAccessible: false,
        findings: []
    };

    console.log(`\n[*] Checking S3 bucket: ${bucketName}`);

    try {
        // 1. Check Public Access Block Configuration
        // This is the primary control for preventing public access.
        const publicAccessBlockCommand = new GetPublicAccessBlockCommand({ Bucket: bucketName });
        const publicAccessBlock = await client.send(publicAccessBlockCommand);
        status.publicAccessBlockConfig = publicAccessBlock.PublicAccessBlockConfiguration;

        if (publicAccessBlock.PublicAccessBlockConfiguration) {
            const { BlockPublicAcls, IgnorePublicAcls, BlockPublicPolicy, RestrictPublicBuckets } = publicAccessBlock.PublicAccessBlockConfiguration;
            if (BlockPublicAcls === false || IgnorePublicAcls === false || BlockPublicPolicy === false || RestrictPublicBuckets === false) {
                status.findings.push("Public Access Block settings are not fully restrictive.");
                status.isPubliclyAccessible = true;
            }
            console.log(`    Public Access Block: ${JSON.stringify(status.publicAccessBlockConfig)}`);
        } else {
            status.findings.push("No Public Access Block configuration found (default allows public access). This is a critical misconfiguration.");
            status.isPubliclyAccessible = true;
        }

    } catch (error: any) {
        if (error.name === "NoSuchPublicAccessBlockConfiguration") {
            status.findings.push("No Public Access Block configuration found. This means public access is not explicitly blocked.");
            status.isPubliclyAccessible = true;
        } else if (error.name === "AccessDenied") {
            status.findings.push(`Access Denied to get Public Access Block for ${bucketName}. Cannot determine full status.`);
        } else {
            console.error(`    Error getting Public Access Block for ${bucketName}: ${error.message}`);
        }
    }

    try {
        // 2. Check Bucket Policy
        // A bucket policy can grant public read/write access.
        const policyCommand = new GetBucketPolicyCommand({ Bucket: bucketName });
        const policyResponse = await client.send(policyCommand);
        const bucketPolicy = JSON.parse(policyResponse.Policy || '{}');
        status.bucketPolicy = bucketPolicy;

        if (bucketPolicy && bucketPolicy.Statement) {
            for (const statement of bucketPolicy.Statement) {
                // Check for statements allowing public access (e.g., Principal: *)
                if (statement.Principal === "*" || (statement.Principal && statement.Principal.AWS === "*")) {
                    if (statement.Effect === "Allow" && (statement.Action === "s3:GetObject" || statement.Action.includes("s3:GetObject"))) {
                        status.findings.push("Bucket policy allows public read access (s3:GetObject).");
                        status.isPubliclyAccessible = true;
                    }
                    if (statement.Effect === "Allow" && (statement.Action === "s3:PutObject" || statement.Action.includes("s3:PutObject"))) {
                        status.findings.push("Bucket policy allows public write access (s3:PutObject) - CRITICAL!");
                        status.isPubliclyAccessible = true;
                    }
                }
            }
        }
        console.log(`    Bucket Policy: ${JSON.stringify(status.bucketPolicy)}`);

    } catch (error: any) {
        if (error.name === "NoSuchBucketPolicy") {
            console.log(`    No bucket policy found for ${bucketName}.`);
        } else if (error.name === "AccessDenied") {
            status.findings.push(`Access Denied to get Bucket Policy for ${bucketName}. Cannot determine full status.`);
        } else {
            console.error(`    Error getting Bucket Policy for ${bucketName}: ${error.message}`);
        }
    }

    try {
        // 3. Check Bucket ACLs (Access Control Lists)
        // ACLs can also grant public read/write access.
        const aclCommand = new GetBucketAclCommand({ Bucket: bucketName });
        const aclResponse = await client.send(aclCommand);
        status.aclGrants = aclResponse.Grants;

        if (aclResponse.Grants) {
            for (const grant of aclResponse.Grants) {
                if (grant.Grantee?.URI === "http://acs.amazonaws.com/groups/global/AllUsers") {
                    if (grant.Permission === "READ" || grant.Permission === "WRITE") {
                        status.findings.push(`Bucket ACL allows public ${grant.Permission.toLowerCase()} access.`);
                        status.isPubliclyAccessible = true;
                    }
                }
            }
        }
        console.log(`    Bucket ACLs: ${JSON.stringify(status.aclGrants)}`);

    } catch (error: any) {
        if (error.name === "AccessDenied") {
            status.findings.push(`Access Denied to get Bucket ACLs for ${bucketName}. Cannot determine full status.`);
        } else {
            console.error(`    Error getting Bucket ACLs for ${bucketName}: ${error.message}`);
        }
    }

    if (status.isPubliclyAccessible) {
        console.log(`[!!!] Bucket ${bucketName} IS PUBLICLY ACCESSIBLE. Findings:`);
        status.findings.forEach(f => console.log(`    - ${f}`));
    } else {
        console.log(`[+] Bucket ${bucketName} is NOT publicly accessible based on checks.`);
    }

    return status;
}

// --- Example Usage ---
async function main() {
    const bucketsToCheck = [
        "my-sensitive-data-bucket", // Replace with actual bucket names
        "my-public-website-bucket",
        "another-private-bucket"
    ];

    for (const bucket of bucketsToCheck) {
        await checkS3BucketPublicAccess(bucket);
    }

    console.log("\n--- Important Considerations ---");
    console.log("1. This script requires AWS credentials with s3:GetBucketPolicy, s3:GetPublicAccessBlock, and s3:GetBucketAcl permissions.");
    console.log("2. It checks for common public access configurations. Other misconfigurations (e.g., IAM policies, cross-account access) could still lead to unintended access.");
    console.log("3. Always verify findings manually and consult AWS documentation for the latest security best practices.");
}

// To run this example:
// 1. Ensure you have AWS SDK v3 installed: `npm install @aws-sdk/client-s3`
// 2. Configure your AWS credentials (e.g., via AWS CLI, environment variables).
// 3. Compile and run: `tsc aws-s3-misconfig.ts && node aws-s3-misconfig.js`

// main().catch(err => {
//     console.error("An error occurred during S3 bucket checks:", err);
// });

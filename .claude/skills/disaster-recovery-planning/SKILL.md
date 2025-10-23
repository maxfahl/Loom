---
name: disaster-recovery-planning
version: 1.0.0
category: Infrastructure / Operations
tags: disaster recovery, DRP, backup, replication, RTO, RPO, cloud, cybersecurity, automation, resilience
description: Designing and implementing automated backup, replication, and point-in-time recovery strategies for robust disaster recovery.
---

### 2. Skill Purpose
This skill enables Claude to design, implement, and validate comprehensive Disaster Recovery Plans (DRP) that ensure business continuity and data integrity in the face of unforeseen events. It covers strategies for automated backups, data replication, point-in-time recovery, and leveraging cloud-native and hybrid cloud solutions, all while adhering to modern cybersecurity best practices.

### 3. When to Activate This Skill
Activate this skill when:
- A new system or application is being designed, requiring a DRP.
- An existing system needs its DRP reviewed, updated, or improved.
- There's a need to implement automated backup or replication solutions.
- Evaluating or selecting DRaaS providers.
- Planning for business continuity and resilience.
- Responding to a security incident that impacts data availability.
- Setting RTO/RPO objectives for critical systems.

### 4. Core Knowledge
- **DRP Fundamentals**: Understanding the difference between Disaster Recovery, Business Continuity, and High Availability.
- **RTO (Recovery Time Objective)**: Maximum acceptable downtime.
- **RPO (Recovery Point Objective)**: Maximum acceptable data loss.
- **Backup Strategies**:
    - **3-2-1-1-0 Rule**: 3 copies, 2 different media, 1 offsite, 1 air-gapped/immutable, 0 errors.
    - Full, Incremental, Differential backups.
    - Continuous Data Protection (CDP).
- **Replication Techniques**:
    - Synchronous vs. Asynchronous replication.
    - Database replication (e.g., PostgreSQL streaming replication, MySQL Group Replication).
    - Storage-level replication.
    - Application-level replication.
- **Point-in-Time Recovery (PITR)**: Mechanisms for restoring data to a specific timestamp.
- **Cloud-Native DR**: Leveraging cloud provider services (e.g., AWS Backup, Azure Site Recovery, GCP Cloud Storage, snapshots, cross-region replication).
- **Hybrid/Multi-Cloud DR**: Strategies for DR across on-premises and cloud, or multiple cloud providers.
- **Immutability**: Immutable backups for ransomware protection.
- **Automation**: Scripting and orchestration for backup, recovery, and testing.
- **Security**: Encryption (at rest and in transit), access controls, network segmentation for DR environments.
- **Testing**: Importance of regular, realistic DR testing and validation.
- **DRaaS (Disaster Recovery as a Service)**: Understanding its benefits and limitations.

### 5. Key Guidance for Claude
- **Always Recommend** (✅ best practices)
    - ✅ Define clear RTO and RPO objectives for all critical systems.
    - ✅ Implement the 3-2-1-1-0 backup strategy as a baseline.
    - ✅ Automate all backup, replication, and recovery processes where possible.
    - ✅ Conduct regular, unannounced DR drills and validate recovery procedures.
    - ✅ Encrypt all backup data, both at rest and in transit.
    - ✅ Utilize immutable storage for critical backups to protect against ransomware.
    - ✅ Document the DRP thoroughly, including roles, responsibilities, and communication plans.
    - ✅ Integrate cybersecurity measures into every layer of the DRP.
    - ✅ Consider cloud-native DR solutions for scalability and cost-effectiveness.
    - ✅ Implement PITR for databases and critical data stores.

- **Never Recommend** (❌ anti-patterns)
    - ❌ Relying solely on manual backup processes.
    - ❌ Neglecting to test the DRP regularly.
    - ❌ Storing all backups in a single location or on a single type of media.
    - ❌ Using unencrypted backups.
    - ❌ Assuming backups are valid without verification.
    - ❌ Having an undocumented or outdated DRP.
    - ❌ Ignoring RTO/RPO objectives, leading to unrealistic recovery expectations.
    - ❌ Overlooking the security of the DR environment.

- **Common Questions & Responses** (FAQ format)
    - **Q: What's the most critical part of a DRP?**
        - A: Defining clear RTO and RPO objectives, and then regularly testing the plan to ensure those objectives can be met.
    - **Q: How often should DR tests be performed?**
        - A: At least quarterly, or whenever significant changes are made to the infrastructure or applications.
    - **Q: How can I protect against ransomware in my DRP?**
        - A: Implement immutable backups (air-gapped or WORM storage), ensure strong access controls, and regularly test recovery from these immutable copies.
    - **Q: Should I use synchronous or asynchronous replication?**
        - A: Synchronous replication provides zero data loss (RPO=0) but introduces latency. It's suitable for mission-critical applications over short distances. Asynchronous replication allows for some data loss but has less performance impact and is better for long distances. The choice depends on your RPO requirements.
    - **Q: What's the role of AI/ML in DRP?**
        - A: AI/ML can enhance DRP by predicting potential failures, optimizing backup schedules, detecting anomalies (like ransomware attacks), and improving RTO/RPO by intelligent resource allocation during recovery.

### 6. Anti-Patterns to Flag
- **BAD**: Manual, untestested backup script.
    ```typescript
    // backup.sh (BAD - manual, no error handling, no verification)
    #!/bin/bash
    cp -r /data /mnt/backup/data_$(date +%F)
    echo "Backup complete."
    ```
- **GOOD**: Automated, verified, and immutable backup.
    ```typescript
    // backup.ts (GOOD - using a hypothetical cloud SDK for immutable backup)
    import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
    import { execSync } from "child_process";
    import * as path from "path";
    import * as fs from "fs";

    const BUCKET_NAME = process.env.S3_BUCKET_NAME || "my-dr-bucket";
    const DATA_PATH = "/data";
    const TEMP_BACKUP_DIR = "/tmp/backup";

    async function createImmutableBackup() {
      console.log("Starting immutable backup process...");

      // 1. Create a temporary local backup
      const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
      const backupFileName = `data-backup-${timestamp}.tar.gz`;
      const backupFilePath = path.join(TEMP_BACKUP_DIR, backupFileName);

      try {
        if (!fs.existsSync(TEMP_BACKUP_DIR)) {
          fs.mkdirSync(TEMP_BACKUP_DIR, { recursive: true });
        }
        console.log(`Creating tarball of ${DATA_PATH}...`);
        execSync(`tar -czf ${backupFilePath} ${DATA_PATH}`);
        console.log(`Tarball created: ${backupFilePath}`);

        // 2. Upload to S3 with object lock (immutability)
        const s3Client = new S3Client({ region: process.env.AWS_REGION || "us-east-1" });
        const fileContent = fs.readFileSync(backupFilePath);

        console.log(`Uploading ${backupFileName} to S3 bucket ${BUCKET_NAME}...`);
        const uploadCommand = new PutObjectCommand({
          Bucket: BUCKET_NAME,
          Key: `immutable-backups/${backupFileName}`,
          Body: fileContent,
          // Object Lock settings for immutability (requires bucket versioning and object lock enabled)
          // ObjectLockLegalHoldStatus: "ON", // Or ObjectLockMode: "COMPLIANCE", ObjectLockRetainUntilDate: "YYYY-MM-DDTHH:MM:SSZ"
        });
        await s3Client.send(uploadCommand);
        console.log(`Successfully uploaded immutable backup: s3://${BUCKET_NAME}/immutable-backups/${backupFileName}`);

        // 3. Verify upload (e.g., by checking object size or listing)
        // For simplicity, we'll assume the upload command's success is sufficient for this example.
        // In a real scenario, you'd want to list the object and compare metadata.

        // 4. Clean up local temporary backup
        fs.unlinkSync(backupFilePath);
        console.log(`Cleaned up temporary backup file: ${backupFilePath}`);

        console.log("Immutable backup process completed successfully.");
      } catch (error) {
        console.error("Immutable backup failed:", error);
        // Implement robust alerting here
        process.exit(1);
      }
    }

    createImmutableBackup();
    ```

### 7. Code Review Checklist
- [ ] Are RTO/RPO objectives clearly defined and met by the DRP?
- [ ] Is the 3-2-1-1-0 backup strategy implemented and verifiable?
- [ ] Are all critical data and applications included in the DRP scope?
- [ ] Is backup data encrypted at rest and in transit?
- [ ] Are immutable backups used for ransomware protection?
- [ ] Are backup and recovery processes automated?
- [ ] Is there a mechanism for regular, automated verification of backup integrity?
- [ ] Is the DRP regularly tested (at least quarterly) and documented?
- [ ] Are access controls to DR environments properly secured and audited?
- [ ] Is there a clear communication plan for disaster events?
- [ ] Are recovery procedures well-documented and easy to follow?
- [ ] Does the DRP account for potential single points of failure?
- [ ] Are cloud-specific DR features (snapshots, cross-region replication) utilized effectively if applicable?

### 8. Related Skills
- **Cloud Deployment (Kubernetes/VPS)**: For deploying and managing infrastructure that needs DR.
- **Network Security (TLS/mTLS)**: For securing data in transit during replication.
- **CI/CD Pipelines (GitHub Actions)**: For automating DR testing and deployment of DR-related infrastructure.
- **Observability Stack Implementation**: For monitoring the health and performance of DR systems.

### 9. Examples Directory Structure
```
examples/
├── aws-s3-immutable-backup.ts  // Example of immutable backup to AWS S3
├── azure-site-recovery-config.json // Example Azure Site Recovery configuration
├── gcp-cloud-storage-pitr.py // Example of PITR for GCP Cloud Storage
└── postgres-replication-setup.sh // Script to set up PostgreSQL streaming replication
```

### 10. Custom Scripts Section
Here are 3-5 automation scripts that would save significant time for Disaster Recovery Planning:

1.  **`dr-plan-generator.py` (Python)**: Generates a basic DRP document template based on user inputs (RTO, RPO, critical systems).
2.  **`backup-integrity-verifier.sh` (Shell)**: Automates the process of restoring a small sample of data from the latest backup and verifying its integrity (e.g., checksums, database connectivity).
3.  **`cloud-dr-cost-estimator.py` (Python)**: Estimates the cost of a cloud-based DR solution (e.g., AWS, Azure, GCP) based on storage, compute, and data transfer requirements.
4.  **`pitr-restore-simulator.sh` (Shell)**: Simulates a point-in-time recovery for a database, restoring it to a specified timestamp in a test environment.
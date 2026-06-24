---
title: "Backup and Restore"
parent: "Cloud Operations"
nav_order: 1
description: "Back up and restore a FalkorDB Cloud instance using RDB export and import. Export to a download link, Google Cloud Storage, or Amazon S3. Restore from a file, URL, cloud storage, or another instance. Schedule recurring backups on Pro and Enterprise."
---

# Backup and Restore

FalkorDB Cloud lets you back up and restore an instance from the **Import/Export RDB** tab on the instance page. A backup is an RDB export. A restore is an RDB import. RDB is the binary snapshot format used by FalkorDB.

![The Import/Export RDB tab with the task list and the Export RDB, Import RDB, and Schedules buttons](/images/cloud/backup-restore/import-export-tab.png)

## Before you begin

- The instance must be in the **Running** state.
- Your access depends on your subscription role. Export needs the **root**, **editor**, or **reader** role. Import needs the **root** or **editor** role.
- One backup or restore task runs at a time per instance. A new request while another task is in progress is rejected.
- When you use your own cloud storage, the access credentials are used only to reach your bucket for that task. They are not stored on the task record.

## Export a backup

An export saves a snapshot of your instance to a destination you choose.

1. Open the **Import/Export RDB** tab on your instance.
2. Select **Export RDB**.
3. Choose a destination and fill in the details.
4. Select **Export**.

The task appears in the list. When it completes you can track it under **Output**.

### Temporary link

FalkorDB writes the backup to managed storage and generates a download link. The link is valid for **one hour**.

![Export RDB dialog with Temporary link selected](/images/cloud/backup-restore/export-temporary-link.png)

When the task completes, select **Download** in the **Output** column to retrieve the file.

![Task list showing a completed export with a Download link](/images/cloud/backup-restore/export-task-download.png)

### Google Cloud Storage

FalkorDB writes the backup to your own Google Cloud Storage bucket. Provide the bucket name and a GCP service account key with permission to create objects in that bucket.

![Export RDB dialog with Google Cloud Storage selected](/images/cloud/backup-restore/export-google-cloud-storage.png)

### Amazon S3

FalkorDB writes the backup to your own Amazon S3 bucket. Provide the bucket name, region, and AWS access credentials with permission to create objects in that bucket. A session token is optional.

![Export RDB dialog with Amazon S3 selected](/images/cloud/backup-restore/export-amazon-s3.png)

## Restore from a backup

A restore loads an RDB into your instance.

> **Caution.** The instance is erased before the import takes place. FalkorDB takes a safety backup of the current data before clearing it, and verifies the imported key count after the load.

1. Open the **Import/Export RDB** tab on your instance.
2. Select **Import RDB**.
3. Choose a source and fill in the details.
4. Select **Import**.

### Upload a file

Upload an RDB file from your local machine.

![Import RDB dialog with Upload file selected and the erase caution](/images/cloud/backup-restore/import-upload-file.png)

### URL

Provide a public HTTPS URL to the RDB file. The URL must use HTTPS and must not point to a private or internal address. FalkorDB checks that the file is reachable before it starts.

### Google Cloud Storage

Read the RDB from your own Google Cloud Storage bucket. Provide the bucket name, the RDB file path, and a GCP service account key with permission to read objects from that bucket.

![Import RDB dialog with Google Cloud Storage selected](/images/cloud/backup-restore/import-google-cloud-storage.png)

### Amazon S3

Read the RDB from your own Amazon S3 bucket. Provide the bucket name, the RDB file path, the region, and AWS access credentials with permission to read objects from that bucket. A session token is optional.

![Import RDB dialog with Amazon S3 selected](/images/cloud/backup-restore/import-amazon-s3.png)

### Another instance

Clone the data from another running FalkorDB Cloud instance. FalkorDB checks that the source data fits the destination before it starts.

## Scheduled backups

Scheduled backups are available on the **Pro** and **Enterprise** tiers. On lower tiers the **Schedules** button is disabled.

Open **Schedules** from the **Import/Export RDB** tab to create and manage them.

- Set how often the backup runs. The period is at least **60 minutes** and a multiple of 15.
- Set the minute of the hour the backup starts. The choices are **0, 15, 30, or 45**.
- You can keep up to **2 schedules** per instance.
- A schedule is disabled automatically after **3 consecutive failures**.

A scheduled export supports the same destinations as a one off export. A scheduled restore clones from another instance.

## Task history

The task list on the **Import/Export RDB** tab shows your past exports and imports. Each row shows the task type, the source or destination, the status, the timestamps, and the output. Statuses move from **created** to **pending**, **in_progress**, and then **completed** or **failed**.

## Limits

| Item | Value |
| :--- | :--- |
| Concurrent tasks per instance | 1 |
| Instance state required | Running |
| Scheduled backups | Pro and Enterprise only |
| Schedules per instance | Up to 2 |
| Schedule period | 60 minutes or more, multiple of 15 |
| Schedule start minute | 0, 15, 30, or 45 |
| Schedule auto disable | After 3 consecutive failures |
| Temporary download link validity | 1 hour |
| Upload link validity | 1 hour |
| Restore size | Must fit the destination capacity |

## Getting Support

Questions about a backup or restore? Email **[support@falkordb.com](mailto:support@falkordb.com)**. See the [Support page](/support/) for what to include in your request.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What is the difference between a backup and a snapshot?"
  a1="A backup on this page is an **RDB export** that you trigger or schedule, sent to a download link or your own cloud storage. Snapshots and automatic backups taken by the platform are managed separately. See your tier page for the automatic backup policy."
  q2="Does a restore overwrite my current data?"
  a2="Yes. The instance is **erased before the import**. FalkorDB takes a safety backup of the current data before clearing it, then verifies the imported key count after the load."
  q3="Which destinations and sources are supported?"
  a3="Export goes to a **temporary download link**, **Google Cloud Storage**, or **Amazon S3**. Import reads from an **uploaded file**, a **URL**, **Google Cloud Storage**, **Amazon S3**, or **another instance**."
  q4="Can I schedule backups on any tier?"
  a4="Scheduled backups are available on the **Pro** and **Enterprise** tiers. On lower tiers the Schedules button is disabled."
  q5="Are my cloud storage credentials stored?"
  a5="No. Credentials you enter for your own bucket are used only to reach that bucket for the task. They are not kept on the task record."
%}

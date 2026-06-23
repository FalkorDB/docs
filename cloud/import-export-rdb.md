---
title: "Import/Export RDB"
parent: "Features"
nav_order: 1
description: "Import and export RDB snapshots for FalkorDB Cloud instances — supports S3, GCS, file upload, and scheduled jobs for Pro and Enterprise tiers."
---

# Import/Export RDB

FalkorDB Cloud lets you export and import RDB snapshots directly from the dashboard. This feature supports manual one-time operations and, on Pro and Enterprise tiers, scheduled recurring jobs.

## Accessing the Feature

1. Log in to the [FalkorDB Dashboard](https://app.falkordb.cloud).
2. Select a **running instance** from your instance list.
3. Open the **Import/Export RDB** tab.

---

## Export

Export your instance's RDB snapshot to an external destination or generate a temporary download link.

### Temporary URL

Generates a pre-signed download URL that is valid for **1 hour**. Use this for quick, one-off transfers without requiring a storage bucket.

### Google Cloud Storage (GCS)

Export the snapshot directly to a GCS bucket. Provide your bucket name and the destination path (object prefix) inside the bucket.

### Amazon S3

Export the snapshot directly to an S3 bucket. Provide your bucket name, region, and the destination path inside the bucket.

---

## Import

Import an RDB snapshot into your instance from a file or an external source.

> ⚠️ **The instance is flushed before the import begins.** All existing data will be deleted.
>
> If the import fails, the instance is automatically restarted with the data that existed before the import.

### Upload File

Upload an RDB file directly from your local machine. Files up to **2 GB** are supported.

### Google Cloud Storage (GCS)

Import an RDB file stored in a GCS bucket. Provide the bucket name and the full object path to the RDB file.

### Amazon S3

Import an RDB file stored in an S3 bucket. Provide the bucket name, region, and the full object path to the RDB file.

### Another Instance

Import the RDB snapshot from another FalkorDB Cloud instance in your account. Select the source instance from the list of available instances.

---

## Scheduled Import/Export

{: .note }
Scheduled import/export jobs are available on **Pro and Enterprise** tiers only.

Automate recurring RDB exports or imports by creating a scheduled job. Only **one scheduled import job** can be active at a time.

### Schedule Configuration

| Parameter | Details |
| :--- | :--- |
| **Period** | Frequency in hours (minimum **1 hour**) |
| **Start minute** | Minute offset within the hour — one of **0**, **15**, **30**, or **45** |

### Scheduled Export

Export your RDB snapshot on a recurring schedule to one of the following destinations:

- **Google Cloud Storage (GCS)**
- **Amazon S3**

### Scheduled Import

Import an RDB snapshot on a recurring schedule from one of the following sources:

- **Google Cloud Storage (GCS)**
- **Amazon S3**
- **Another instance** — pulls the latest RDB snapshot from a selected FalkorDB Cloud instance

> ⚠️ Only one scheduled import job can be created per instance.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What happens to my data when I import an RDB file?"
  a1="The instance is **flushed** (all existing data is deleted) before the import begins. If the import fails for any reason, the instance is automatically restarted with the data it had before the import."
  q2="How large can an uploaded RDB file be?"
  a2="You can upload RDB files up to **2 GB** directly from your browser. For larger datasets, use GCS or S3 as the import source."
  q3="How long is the temporary export URL valid?"
  a3="Temporary download URLs are valid for **1 hour** from the time they are generated."
  q4="Can I automate recurring backups?"
  a4="Yes. Scheduled import/export jobs are available on **Pro and Enterprise** tiers. You can configure the frequency in hours (minimum 1 hour) and choose the start minute (0, 15, 30, or 45)."
  q5="How many scheduled import jobs can I create?"
  a5="Only **one scheduled import job** can be active per instance at a time."
%}

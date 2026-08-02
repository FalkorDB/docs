---
title: "UDF Libraries"
description: "Manage JavaScript UDF libraries: load, inspect, remove, and export function bundles."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 15
---

# UDF Libraries
The UDF Libraries page (`/udf`) is used to manage JavaScript user-defined function libraries available to FalkorDB.

![UDF libraries page](../../images/browser/udf-libraries.png)

## What you can do
- **Load Lib**
  - Upload a UDF library file and register it on the server.
- **Flush Libs**
  - Remove loaded libraries from the current environment.
- **Browse libraries**
  - View currently loaded library names in the left panel.
- **Inspect code**
  - Open a loaded library and review its source in the editor area.
- **Export**
  - Download the currently viewed library source.

## Typical workflow
1. Open **/udf** from the left navigation.
2. Click **Load Lib** and select your JavaScript UDF file.
3. Confirm the library appears in the **Libraries** list.
4. Click the library entry to inspect its code.
5. Use **Export** if you need to download the current source.

## Notes
- UDF behavior depends on server-side support and permissions.
- If you do not see expected libraries, verify your connection and user role.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Where do I manage user-defined functions in Browser?"
  a1="Use the **UDF Libraries** page at `/udf`, accessible from the left navigation."
  q2="What file format should I upload with Load Lib?"
  a2="Upload a JavaScript UDF library file that follows FalkorDB UDF conventions."
  q3="What does Flush Libs do?"
  a3="It clears loaded UDF libraries from the current environment."
  q4="Can I view and download library code from the UI?"
  a4="Yes. Select a library to view its source, then use **Export** to download it."
%}

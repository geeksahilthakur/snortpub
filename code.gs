/**
 * ==================================================
 * PROJECT: SNORT BRIDGE FINAL (Production Ready)
 * DEVELOPER: geeksahil
 * FEATURES: Type Fixing, Anti-Spam, Custom Links
 * ==================================================
 */

function doPost(e) {
  var lock = LockService.getScriptLock();

  try {
    lock.waitLock(10000);
  } catch (e) {
    return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Server busy"}));
  }

  try {
    // 1. VALIDATION
    if (!e || !e.postData || !e.postData.contents) {
      return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "No data received"}));
    }

    var requestData = JSON.parse(e.postData.contents);
    var rawLog = requestData.log_line;

    // CRITICAL: Check the Anti-Flood Flag from Python
    var shouldSendEmail = requestData.send_email;

    if (!rawLog) {
      return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Missing log_line"}));
    }

    // 2. DATA CLEANING
    // Split the CSV: [0]Time, [1]Msg, [2]Proto, [3]Src, [4]SrcPort, [5]Dst, [6]DstPort
    var columns = rawLog.trim().split(',').map(function(item) {
      return item ? item.trim() : "";
    });

    // --- FIX: CONVERT PORTS TO NUMBERS ---
    // Google Sheets complains if you put text "80" into a Number column.
    // We force them to be integers here.
    if (columns[4] && !isNaN(parseInt(columns[4]))) {
      columns[4] = parseInt(columns[4]); // Source Port
    }
    if (columns[6] && !isNaN(parseInt(columns[6]))) {
      columns[6] = parseInt(columns[6]); // Dest Port
    }

    // Add Server Timestamp
    var now = new Date();
    var timestampStr = Utilities.formatDate(now, Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss");
    columns.push(timestampStr);

    // 3. WRITE TO SHEET
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    sheet.appendRow(columns);

    // 4. SEND EMAIL (Conditional)
    // Only send if Python says True (Anti-Flood)
    if (shouldSendEmail === true) {
      try {
        sendProfessionalEmail(columns);
      } catch (emailError) {
        console.error("Email failed: " + emailError.toString());
      }
    }

    return ContentService.createTextOutput(JSON.stringify({
      "status": "success",
      "row": sheet.getLastRow(),
      "email_sent": shouldSendEmail
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": error.toString()})).setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

/**
 * Sends the HTML Email with the corrected link.
 */
function sendProfessionalEmail(data) {
  var recipient = "itssahilthakur@gmail.com";

  // Data Mapping
  var alertMsg = data[1] || "Security Alert";
  var proto = data[2] || "Unknown";
  var attackerIP = data[3] || "N/A";
  var attackerPort = data[4] || "";

  // YOUR DASHBOARD LINK
  var sheetLink = "https://docs.google.com/spreadsheets/d/1r2YzwCA3SwObfn0VJhOUExIy7EUH5t3h7eSVnGOgZnU/edit?gid=0#gid=0";

  var subject = "🚨 Threat Detected: " + alertMsg + " (" + attackerIP + ")";

  var htmlBody = `
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">

      <!-- HEADER -->
      <div style="background-color: #d32f2f; color: white; padding: 25px; text-align: center;">
        <h2 style="margin: 0; font-size: 22px; text-transform: uppercase; letter-spacing: 1px;">Intrusion Alert</h2>
        <p style="margin: 5px 0 0; opacity: 0.9;">SnortPub Monitor</p>
      </div>

      <!-- BODY -->
      <div style="padding: 30px; background-color: #ffffff;">
        <p style="font-size: 16px; color: #333; margin-bottom: 20px;">
          The Snort sensor has detected suspicious activity on your network.
        </p>

        <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 25px;">
          <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 10px; font-weight: bold; color: #555; width: 35%;">Threat Type</td>
            <td style="padding: 10px; color: #d32f2f; font-weight: bold;">${alertMsg}</td>
          </tr>
          <tr style="border-bottom: 1px solid #eee; background-color: #f9f9f9;">
            <td style="padding: 10px; font-weight: bold; color: #555;">Source IP</td>
            <td style="padding: 10px;">${attackerIP}</td>
          </tr>
          <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 10px; font-weight: bold; color: #555;">Source Port</td>
            <td style="padding: 10px;">${attackerPort}</td>
          </tr>
          <tr style="border-bottom: 1px solid #eee; background-color: #f9f9f9;">
            <td style="padding: 10px; font-weight: bold; color: #555;">Protocol</td>
            <td style="padding: 10px;">${proto}</td>
          </tr>
          <tr>
            <td style="padding: 10px; font-weight: bold; color: #555;">Timestamp</td>
            <td style="padding: 10px;">${data[0]}</td>
          </tr>
        </table>

        <!-- BUTTON -->
        <div style="text-align: center;">
           <a href="${sheetLink}" style="display: inline-block; background-color: #1976d2; color: white; padding: 12px 28px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 14px;">View Full Logs</a>
        </div>
      </div>

      <!-- FOOTER -->
      <div style="background-color: #f5f5f5; padding: 15px; text-align: center; font-size: 12px; color: #888; border-top: 1px solid #e0e0e0;">
        <p style="margin: 0;">Automated Security Notification</p>
        <p style="margin: 5px 0 0; font-weight: bold; color: #555;">developer : geeksahil</p>
      </div>
    </div>
  `;

  MailApp.sendEmail({
    to: recipient,
    subject: subject,
    htmlBody: htmlBody
  });
}
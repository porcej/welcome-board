# Digital Signage Welcome Board - User Tutorial

This tutorial will guide you through customizing your dashboard, managing icons, and working with schedules.

## Table of Contents

1. [Customizing Dashboard Settings](#customizing-dashboard-settings)
2. [Managing Icons](#managing-icons)
3. [Creating Schedules](#creating-schedules)
4. [Adding Schedule Items](#adding-schedule-items)
5. [Updating Schedules](#updating-schedules)
6. [Exporting Schedules](#exporting-schedules)
7. [Importing Schedules](#importing-schedules)

---

## Customizing Dashboard Settings

The Settings page allows you to customize the appearance and behavior of your digital sign display.

### Accessing Settings

1. Log in to the application
2. Navigate to **Schedules** → **Settings** (or click the Settings link in the navigation)

### Uploading Logo

1. In the **Logo** field, click "Choose File" and select an image file (PNG, JPG, JPEG, or GIF)
2. Set the **Logo Size** (50-500 pixels) - this is the maximum height in pixels
3. Click **Save Settings**
4. Your logo will appear at the top of the display

**Tip**: Use a transparent PNG for best results. Recommended size: 200-300 pixels wide.

### Setting Background Image

1. In the **Background Image** field, click "Choose File" and select an image (PNG, JPG, JPEG, GIF, or WEBP)
2. Choose how the image should be displayed:
   - **Tile**: Repeats the image to fill the screen
   - **Stretch**: Stretches the image to fill the entire screen
   - **Fit**: Scales the image to fit while maintaining aspect ratio
   - **Center**: Displays the image at its original size, centered
3. Click **Save Settings**

**Tip**: For best results, use high-resolution images (1920x1080 or higher) for full-screen displays.

### Customizing Colors

You can customize the color scheme of your display:

1. **Background Color**: Main background color (default: black #000000)
2. **Text Color**: Primary text color (default: white #ffffff)
3. **Side Panel Color**: Color for the left side panel (default: dark gray #212529)
4. **Side Panel Opacity**: Transparency level (0.0 = fully transparent, 1.0 = fully opaque)
5. **Schedule Box Color**: Color for the schedule display box (default: dark gray #212529)
6. **Schedule Box Opacity**: Transparency level for the schedule box

To change a color:
1. Click the color picker next to the color field
2. Select your desired color
3. Adjust opacity using the number field (0.0 to 1.0)
4. Click **Save Settings**

### Configuring Weather Display

To show weather information on your display:

1. Enter your **Latitude** (e.g., 40.7128 for New York)
2. Enter your **Longitude** (e.g., -74.0060 for New York)
3. Enter your **Timezone** (e.g., America/New_York, Europe/London, UTC)
   - Use standard timezone names from the [IANA Time Zone Database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
4. Click **Save Settings**

**Finding Your Coordinates**: 
- Use Google Maps: Right-click on your location → Click the coordinates to copy them
- Or use an online tool like [latlong.net](https://www.latlong.net/)

### Adding Left Column Notes

You can add custom text that appears in the left column of the display:

1. Enter your notes in the **Left Column Notes** field
2. You can use multiple lines
3. Click **Save Settings**

**Tip**: Use this for announcements, contact information, or other static content.

---

## Managing Icons

Icons can be used to visually identify schedule items. You can create icons from images or use text characters.

### Creating an Image-Based Icon

1. Navigate to **Icons** → **New Icon**
2. Enter an **Icon Name** (e.g., "Meeting", "Training", "Event")
3. Leave **Use Text Instead of Image** unchecked
4. Click **Choose File** and select an image file (PNG, JPG, JPEG, GIF, or WEBP)
5. Check **Enabled** to make the icon available for use
6. Click **Save**

**Tip**: Use small, simple icons (64x64 or 128x128 pixels) for best display results.

### Creating a Text-Based Icon

1. Navigate to **Icons** → **New Icon**
2. Enter an **Icon Name** (e.g., "Warning", "Star", "Check")
3. Check **Use Text Instead of Image**
4. Enter **Characters** (e.g., ⚠, ★, ✓, ⚡, 🎯)
   - You can use emoji, special characters, or Unicode symbols
5. Select a **Font** from the dropdown
6. Check **Enabled** to make the icon available
7. Click **Save**

**Tip**: Test different fonts to see which displays best on your screen. Some fonts work better with certain characters.

### Editing or Disabling Icons

1. Navigate to **Icons**
2. Click on an icon name to edit it
3. Make your changes
4. Uncheck **Enabled** to temporarily disable an icon (it won't be deleted, just hidden)
5. Click **Save**

---

## Creating Schedules

Schedules organize your events and activities. Each schedule can contain multiple items.

### Creating a New Schedule

1. Navigate to **Schedules** → **New**
2. Enter a **Schedule Name** (e.g., "Monday Schedule", "Weekend Events", "Special Event")
3. **Date** (Optional):
   - If you want the schedule to automatically activate on a specific date, select that date
   - If you leave it blank, you'll need to manually activate it using the "Active" checkbox
4. **Active** checkbox:
   - Check this to immediately activate the schedule (only needed if no date is set)
   - Only one schedule can be active at a time
5. **Show Name on Display**: Check this to display the schedule name on the digital sign
6. Click **Save**

**Understanding Date-Based Activation**:
- **With Date**: The schedule will automatically display on that specific date, regardless of the "Active" checkbox
- **Without Date**: The schedule only displays when "Active" is checked

**Example**: If you create a schedule with today's date, it will automatically show on the display today, even if "Active" is unchecked.

### After Creating a Schedule

After saving, you'll be taken to the schedule edit page where you can:
- Add schedule items (see next section)
- Export the schedule to Excel
- Duplicate the schedule
- Delete the schedule

---

## Adding Schedule Items

Schedule items are the individual events or activities within a schedule.

### Creating a Schedule Item

1. Open a schedule (create new or edit existing)
2. Click **Add Item**
3. Fill in the item details:

   **Required Fields**:
   - **Start Time**: When the item begins (format: HH:MM, e.g., 09:00, 14:30)
   - **Duration (minutes)**: How long the item lasts (optional, but recommended)
   
   **Optional Fields**:
   - **Name**: Item name or title
   - **Location**: Where the item takes place
   - **Uniform**: Required uniform or dress code
   - **Lead**: Person leading or responsible for the item
   - **Notes**: Additional information or instructions
   - **Icon**: Select an icon to display with this item

4. Click **Save**

**Tip**: If you provide a duration, the end time will be calculated automatically. Otherwise, you can manually set an end time.

### Example Schedule Item

- **Name**: Morning Briefing
- **Start Time**: 08:00
- **Duration**: 30 minutes
- **Location**: Conference Room A
- **Lead**: John Smith
- **Notes**: All staff required
- **Icon**: Meeting

This will display as: "08:00 - 08:30 📍 Conference Room A 👤 John Smith 📝 All staff required"

### Editing or Deleting Items

1. From the schedule edit page, find the item in the list
2. Click **Edit** to modify the item
3. Click **Delete** to remove the item (you'll be asked to confirm)

---

## Updating Schedules

### Editing Schedule Details

1. Navigate to **Schedules**
2. Click on the schedule name you want to edit
3. Modify any fields:
   - Change the name
   - Update the date (or remove it)
   - Toggle the "Active" status
   - Change "Show Name on Display" setting
4. Click **Save**

### Changing Active Schedule

Only one schedule can be active at a time (for schedules without dates):

1. Open the schedule you want to activate
2. Check the **Active** checkbox
3. Click **Save**
4. The previously active schedule will automatically be deactivated

**Note**: If a schedule has a date set and it matches today's date, it will automatically be active regardless of the checkbox.

### Duplicating a Schedule

To create a copy of an existing schedule:

1. Open the schedule you want to duplicate
2. Click the **📋 Duplicate** button
3. A new schedule will be created with "(Copy)" appended to the name
4. The duplicate will not be active by default
5. Edit the duplicate to change the name, date, or items as needed

**Use Case**: Great for creating weekly schedules - create one Monday schedule, duplicate it, and modify for other days.

### Deleting a Schedule

1. Open the schedule you want to delete
2. Click the **Delete** button
3. Confirm the deletion
4. **Warning**: This will also delete all items in the schedule

---

## Exporting Schedules

Exporting allows you to backup schedules, share them, or edit them in Excel.

### Exporting to Excel

1. Navigate to **Schedules**
2. Open the schedule you want to export
3. Click **Export to Excel** (or use the button at the top of the schedule edit page)
4. The file will download with a name like: `schedule_Schedule_Name_20231203.xlsx`

### What Gets Exported

The Excel file includes:
- Schedule metadata (name, date, active status, show name setting)
- All schedule items with:
  - Name
  - Start Time
  - End Time
  - Duration
  - Location
  - Uniform
  - Lead
  - Notes
  - Icon

### Using Exported Files

- **Backup**: Keep exported files as backups
- **Editing**: Open in Excel, make changes, then import back
- **Sharing**: Send to colleagues who can import into their system
- **Bulk Editing**: Easier to edit many items in Excel than one-by-one in the web interface

---

## Importing Schedules

You can import schedules from Excel files, either files exported from this system or manually created files.

### Importing an Exported Schedule

1. Navigate to **Schedules** → **Import**
2. Click **Choose File** and select an Excel file (.xlsx or .xls)
3. Click **Import**
4. The schedule will be created with all items

### Creating an Import File from Scratch

If you want to create a schedule in Excel and import it, follow this format:

**Row 1, Column B**: Schedule Name (e.g., "Monday Schedule")
**Row 2, Column B**: Date in YYYY-MM-DD format (e.g., "2024-12-03") or "Not specified"
**Row 3, Column B**: Active status - "Yes" or "No"
**Row 4, Column B**: Show Name - "Yes" or "No"
**Row 5**: Leave empty
**Row 6**: Headers (in this order):
- Name
- Start Time
- End Time
- Duration (min)
- Location
- Uniform
- Lead
- Notes
- Icon

**Row 7 and below**: Schedule items (one per row)

### Import File Format Example

```
| Column A      | Column B           |
|---------------|--------------------|
| Schedule Name:| Monday Schedule     |
| Date:         | 2024-12-03         |
| Active:       | Yes                 |
| Show Name:    | Yes                 |
|               |                    |
| Name          | Start Time | ...   |
| Briefing      | 08:00      | ...   |
| Training      | 10:00      | ...   |
```

### Import Tips

1. **Time Format**: Use 24-hour format (HH:MM), e.g., "08:00", "14:30"
2. **Date Format**: Use YYYY-MM-DD format, e.g., "2024-12-03"
3. **Empty Fields**: Leave cells empty if a field doesn't apply
4. **Icons**: Use exact icon names as they appear in your Icons list
5. **Duration**: Enter as a number (minutes), e.g., "30" for 30 minutes

### Troubleshooting Imports

- **"Invalid file type"**: Make sure you're using .xlsx or .xls format
- **"Error importing schedule"**: Check that your date format is correct (YYYY-MM-DD)
- **Missing items**: Ensure Row 6 has the correct headers in the correct order
- **Time errors**: Use 24-hour format (HH:MM) without AM/PM

---

## Quick Reference

### Schedule Workflow

1. **Create Schedule** → Set name and optional date
2. **Add Items** → Add all schedule items with times and details
3. **Activate** → Check "Active" (if no date) or set date to today
4. **View Display** → Check `/display` to see your schedule

### Best Practices

- **Naming**: Use descriptive schedule names (e.g., "Monday Morning", "Weekend Events")
- **Dates**: Set dates for one-time events, leave blank for recurring schedules
- **Icons**: Create icons before adding schedule items for better organization
- **Backup**: Regularly export schedules as backups
- **Testing**: Always check the display after making changes

### Common Tasks

- **Weekly Schedule**: Create 7 schedules (one per day) with dates set
- **Recurring Schedule**: Create without date, activate manually when needed
- **Special Event**: Create with specific date, will auto-activate on that day
- **Template**: Create a schedule, duplicate it, then modify for variations

---

## Getting Help

If you encounter issues:

1. Check that all required fields are filled
2. Verify date formats (YYYY-MM-DD)
3. Ensure time formats are correct (HH:MM, 24-hour)
4. Check that icons exist before using them in items
5. Verify file formats when importing (must be .xlsx or .xls)

For technical support, contact your system administrator.


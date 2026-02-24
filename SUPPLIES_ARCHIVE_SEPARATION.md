# Supplies Archive Separation Fix

## Problem Solved
Supplies with "Not Functional" condition were appearing in BOTH the main Supplies table AND the Archive tab. They should only appear in the Archive tab once they are marked as not functional.

## Solution Implemented

### Frontend Changes (Staff-Inventory.html)

**Updated `filteredSupplies` Computed Property** (Lines 1634-1660):

The main supplies table now **excludes** supplies with archived conditions using **case-insensitive** matching:

```javascript
get filteredSupplies() {
    // Exclude supplies that should be in Archive
    const activeSupplies = (this.supplies || []).filter(supply => {
        const condition = (supply.condition_status || supply.condition || '').toLowerCase();
        
        // Exclude archived conditions (case-insensitive)
        const isArchived = condition === 'not functional' || 
                         condition === 'poor' ||
                         condition === 'damaged' || 
                         condition === 'broken' || 
                         condition === 'needs replacement' ||
                         condition === 'disposed' ||
                         condition === 'expired' ||
                         condition === 'not-functional' ||
                         condition === 'for disposal';
        
        return !isArchived; // Return only non-archived supplies
    });
    
    return activeSupplies;
}
```

**Archived Conditions** (Case-Insensitive):
- ❌ Not Functional / not functional / Not-Functional
- ❌ Poor / poor
- ❌ damaged / Damaged
- ❌ broken / Broken
- ❌ needs replacement / Needs Replacement
- ❌ disposed / Disposed / for disposal
- ❌ expired / Expired

### Statistics Cards Updated

All statistics cards now use `filteredSupplies` instead of `supplies`:

1. **Total Supplies Card**: Shows only active supplies count
2. **Medical Equipment Card**: Counts only active medical equipment
3. **Fair Condition Card**: Counts only active supplies in fair condition
4. **Categories Card**: Shows categories from active supplies only

### Archive Tab (Updated)

**Updated `expiredSupplies` Computed Property** (Lines 1717-1735):

The Archive tab now uses **case-insensitive** matching to show archived supplies:

```javascript
get expiredSupplies() {
    return this.supplies.filter(supply => {
        const condition = (supply.condition_status || supply.condition || '').toLowerCase();
        
        // Archive supplies that are not functional (case-insensitive)
        const isArchived = condition === 'not functional' || 
                         condition === 'poor' ||
                         condition === 'damaged' || 
                         condition === 'broken' || 
                         condition === 'needs replacement' ||
                         condition === 'disposed' ||
                         condition === 'expired' ||
                         condition === 'not-functional' ||
                         condition === 'for disposal';
        
        return isArchived;
    });
}
```

## User Workflow

### Before Fix:
1. Supply marked as "Not Functional" ❌
2. Appears in main Supplies table ❌
3. Also appears in Archive tab ❌
4. **Duplicate display** ❌

### After Fix:
1. Supply marked as "Not Functional" ✅
2. **Removed** from main Supplies table ✅
3. **Only** appears in Archive tab ✅
4. **Clean separation** ✅

## Example Scenario

**Supply**: "asdasd" (Medical Equipment)
**Condition**: "Not Functional"

**Before**:
- Supplies Tab: Shows "asdasd" ❌
- Archive Tab: Shows "asdasd" ❌
- Total Count: 7 (includes archived items) ❌

**After**:
- Supplies Tab: Does NOT show "asdasd" ✅
- Archive Tab: Shows "asdasd" ✅
- Total Count: 6 (only active items) ✅

## Technical Details

### Filtering Logic
```javascript
// Main table shows only active supplies (case-insensitive)
filteredSupplies = supplies.filter(s => {
    const condition = s.condition_status.toLowerCase();
    return !isArchived(condition);
})

// Archive tab shows only archived supplies (case-insensitive)
expiredSupplies = supplies.filter(s => {
    const condition = s.condition_status.toLowerCase();
    return isArchived(condition);
})
```

### Case-Insensitive Matching
All condition checks now use `.toLowerCase()` to handle variations:
- "Not Functional" → "not functional"
- "Not-Functional" → "not-functional"
- "POOR" → "poor"
- "Damaged" → "damaged"

### Console Logging
Enhanced logging for debugging:
```
🔍 Supply: asdasd, Condition: "not functional", Archived: true
📦 Total supplies: 7
✅ Active supplies (shown in table): 6
🗄️ Archived supplies: 1
```

## Benefits

1. **Clean Separation**: Clear distinction between active and archived supplies
2. **Accurate Statistics**: Counts reflect only active equipment
3. **No Duplicates**: Each supply appears in only one location
4. **Better Organization**: Easy to find functional vs non-functional items
5. **Proper Archiving**: Archive tab serves its intended purpose

## Files Modified

**Staff-Inventory.html**:
- Lines 1634-1654: Updated `filteredSupplies` computed property with case-insensitive matching
- Lines 1717-1734: Updated `expiredSupplies` computed property with case-insensitive matching
- Lines 1857-1879: Updated `getExpiredSupplyReason()` function to handle all archived conditions
- Line 574: Total Supplies card uses `filteredSupplies.length`
- Line 592: Medical Equipment card uses `filteredSupplies.filter()`
- Line 610: Fair Condition card uses `filteredSupplies.filter()`
- Line 628: Categories card uses `filteredSupplies.map()`
- Line 851: Supplies table uses `filteredSupplies` instead of `supplies`
- Line 910: Empty state check uses `filteredSupplies.length`
- Lines 1114-1122: Archive table header - removed Location and Reason, added Remarks
- Line 1160: Archive table shows `supply.notes` from database as Remarks

## Result

✅ Supplies with "Not Functional" condition removed from main table (case-insensitive)
✅ Archived supplies only appear in Archive tab
✅ Statistics cards show accurate active supply counts
✅ Clean, organized inventory management
✅ No duplicate displays
✅ Handles all condition variations (Not Functional, not functional, Not-Functional, etc.)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the file
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Reports.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line with "return names[dept] || 'All Departments';"
insert_after_line = None
for i, line in enumerate(lines):
    if "return names[dept] || 'All Departments';" in line:
        # Find the closing }, after this
        for j in range(i, min(i+5, len(lines))):
            if lines[j].strip() == '},':
                insert_after_line = j
                break
        if insert_after_line:
            break

if insert_after_line is None:
    print("❌ Could not find insertion point")
    exit(1)

print(f"✅ Found insertion point at line {insert_after_line + 1}")

# The functions to insert
new_functions = """                
                scrollToChart() {
                    if (this.selectedChartFilter === 'all') {
                        this.showAllCharts();
                        return;
                    }
                    document.querySelectorAll('[data-chart-container]').forEach(container => {
                        container.style.display = 'none';
                    });
                    const chartElement = document.getElementById(this.selectedChartFilter);
                    if (chartElement) {
                        const container = chartElement.closest('[data-chart-container]');
                        if (container) {
                            container.style.display = 'block';
                            container.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            container.classList.add('ring-4', 'ring-blue-400', 'ring-opacity-50');
                            setTimeout(() => {
                                container.classList.remove('ring-4', 'ring-blue-400', 'ring-opacity-50');
                            }, 2000);
                        }
                    }
                },
                
                showAllCharts() {
                    document.querySelectorAll('[data-chart-container]').forEach(container => {
                        container.style.display = 'block';
                    });
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                },
                
                resetFilters() {
                    this.selectedChartFilter = 'all';
                    this.selectedPeriod = 'month';
                    this.selectedDepartment = 'all';
                    this.showAllCharts();
                    this.updateCharts();
                },
"""

# Insert the functions
lines.insert(insert_after_line + 1, new_functions)

# Write back
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Reports.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Functions inserted successfully!")
print(f"✅ Inserted after line {insert_after_line + 1}")
